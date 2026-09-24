<template>
  <v-dialog
    :model-value="modelValue"
    max-width="600"
    :persistent="loading || processing"
    @update:model-value="emit('update:modelValue', $event)"
    @after-leave="destroyPaymentElement"
  >
    <v-card variant="outlined" class="account-card bg-surface">
      <v-card-item class="pa-6">
        <template #prepend>
          <v-avatar size="44" class="mr-2">
            <v-icon icon="mdi-credit-card-outline" color="primary" size="40" />
          </v-avatar>
        </template>
        <v-card-title class="font-weight-bold"> Complete payment </v-card-title>
        <v-card-subtitle v-if="plan && plan.id !== 'free'" class="text-medium-emphasis">{{
          plan.title
        }}</v-card-subtitle>
      </v-card-item>
      <v-card-text class="text-body-2 text-medium-emphasis">
        <div ref="paymentElementRef" :class="{ 'payment-element-loading': processing || !paymentElementReady }" />
        <div v-if="!paymentElementReady" class="d-flex flex-column justify-center align-center py-10">
          <v-progress-circular indeterminate color="primary" size="32" class="mb-3" />
          <div>Loading...</div>
        </div>
        <div v-else-if="processing" class="d-flex flex-column justify-center align-center py-10">
          <v-progress-circular indeterminate color="primary" size="32" class="mb-3" />
          <div class="font-weight-bold">Processing payment...</div>
          <div class="mt-4">Please wait while we confirm your payment.</div>
        </div>
        <v-form v-else ref="formRef" class="mt-5" @submit.prevent="submitPayment()">
          <div class="d-flex justify-end ga-3">
            <v-btn
              variant="text"
              color="default"
              size="large"
              class="px-6 font-weight-bold"
              :disabled="loading"
              :loading="subscription.cancelling"
              @click="cancelPayment()"
            >
              Cancel
            </v-btn>
            <v-btn
              v-if="plan && plan.id !== 'free'"
              type="submit"
              color="primary"
              elevation="0"
              size="large"
              :disabled="subscription.cancelling"
              :loading="loading"
              prepend-icon="mdi-credit-card-check-outline"
              class="px-6 font-weight-bold"
            >
              <span class="me-1">Pay</span>
              <b v-if="plan">{{ `${plan.amount} ${plan.currency}` }}</b>
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'

import { stripePromise } from '@/config/stripe'
import { useUiStore } from '@/stores/ui'
import { useSubscriptionStore } from '@/stores/subscription'

const ui = useUiStore()
const subscription = useSubscriptionStore()

const ERROR_OCURRED_MESSAGE = 'An error occurred processing your payment. Please try again later.'
const ERROR_START_MESSAGE = 'We could not start your payment. Please try again later.'
const PROCESSING_INTERVAL_TIMES = 3
const PROCESSING_INTERVAL = 3000

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  plan: {
    type: Object,
    default: null,
  },
  clientSecret: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'success'])

const loading = ref(false)
const processing = ref(false)
const intervalId = ref(null)
const paymentElementRef = ref(null)
const paymentElementReady = ref(false)

let stripe = null
let elements = null
let paymentElement = null

function isActive() {
  const s = subscription.subscriptions.find((s) => (s.plan = props.plan.id))
  return s?.status == 'active'
}

function isPending() {
  const s = subscription.subscriptions.find((s) => (s.plan = props.plan.id))
  return s?.status == 'pending'
}

function isProcessing() {
  const s = subscription.subscriptions.find((s) => (s.plan = props.plan.id))
  return s?.payment_status == 'processing'
}

function isCanceled() {
  const s = subscription.subscriptions.find((s) => (s.plan = props.plan.id))
  return s?.status == 'canceled'
}

async function mountPaymentElement() {
  if (!props.clientSecret) {
    ui.showError(ERROR_START_MESSAGE)
    return
  }

  paymentElementReady.value = false
  await nextTick()

  stripe = await stripePromise
  elements = stripe.elements({
    clientSecret: props.clientSecret,
    appearance: {
      theme: 'stripe',
      variables: {
        colorPrimary: '#4F46E5',
        colorBackground: '#FFFFFF',
        colorText: '#1E293B',
      },
    },
  })
  paymentElement = elements.create('payment')
  paymentElement.on('ready', () => {
    paymentElementReady.value = true
  })
  paymentElement.mount(paymentElementRef.value)
}

async function submitPayment() {
  if (!stripe || !elements) {
    ui.showError(ERROR_START_MESSAGE)
    return
  }

  try {
    loading.value = true
    const { error } = await stripe.confirmPayment({
      elements,
      redirect: 'if_required',
    })
    if (error) {
      if (!['validation_error', 'card_error'].includes(error.type)) {
        throw error
      }
      loading.value = false
      return
    }
  } catch {
    emit('update:modelValue', false)
    ui.showError(ERROR_OCURRED_MESSAGE)
    return
  } finally {
    loading.value = false
  }

  refreshPayment()
}

async function syncPendingPayment() {
  try {
    await subscription.syncPendingPayment()

    if (isProcessing() || !isPending()) {
      if (isActive()) {
        emit('success')
      } else if (isCanceled()) {
        ui.showError(ERROR_OCURRED_MESSAGE)
      }
    }
  } catch {
    ui.showError(ERROR_OCURRED_MESSAGE)
  } finally {
    emit('update:modelValue', false)
  }
}

async function cancelPayment() {
  emit('update:modelValue', false)
  await subscription.cancelPendingSubscription({ confirmation: 'CANCEL' })
  await subscription.listSubscriptions()
}

function refreshPayment() {
  let count = 0
  let loadingRefresh = false

  processing.value = true

  intervalId.value = setInterval(async () => {
    if (loadingRefresh) return

    if (count >= PROCESSING_INTERVAL_TIMES) {
      clearInterval(intervalId.value)

      if (isPending()) {
        // Last request if pending. Try to synchronize directly with stripe.
        return await syncPendingPayment()
      } else {
        emit('update:modelValue', false)
        ui.showError(ERROR_OCURRED_MESSAGE)
        return
      }
    }

    try {
      loadingRefresh = true
      await subscription.listSubscriptions()
      count++

      if (isProcessing() || !isPending()) {
        emit('update:modelValue', false)
        if (isActive()) {
          emit('success')
        } else if (isCanceled()) {
          ui.showError(ERROR_OCURRED_MESSAGE)
        }
      }
    } catch {
      emit('update:modelValue', false)
      ui.showError(ERROR_OCURRED_MESSAGE)
    } finally {
      loadingRefresh = false
    }
  }, PROCESSING_INTERVAL)
}

function destroyPaymentElement() {
  paymentElement?.destroy()
  paymentElement = null
  elements = null
  stripe = null
  loading.value = false
  processing.value = false
  paymentElementReady.value = false
}

watch(
  () => props.modelValue,
  async (open) => {
    if (open) await mountPaymentElement()
  },
)

onBeforeUnmount(destroyPaymentElement)
</script>

<style scoped>
.payment-element-loading {
  visibility: hidden;
  height: 0;
  overflow: hidden;
}
</style>
