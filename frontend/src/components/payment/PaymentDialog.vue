<template>
  <v-dialog
    :model-value="modelValue"
    max-width="600"
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
        <v-card-title class="text-h6 font-weight-bold"> Complete payment </v-card-title>
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
          <div v-if="plan && plan.id !== 'free'" class="d-flex justify-end ga-3">
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
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import { useSubscriptionStore } from '@/stores/subscription'

const ui = useUiStore()
const auth = useAuthStore()
const subscription = useSubscriptionStore()

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
const paymentElementRef = ref(null)
const paymentElementReady = ref(false)

let stripe = null
let elements = null
let paymentElement = null

async function mountPaymentElement() {
  if (!props.clientSecret) {
    ui.showError('We could not start your payment. Please try again later.')
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
    ui.showError('We could not process your payment. Please try again later.')
    return
  }

  loading.value = true
  try {
    const { error } = await stripe.confirmPayment({
      elements,
      redirect: 'if_required',
    })
    if (error) {
      if (!['validation_error', 'card_error'].includes(error.type)) {
        throw error
      }
      return
    }

    processing.value = true
    const data = await subscription.syncPayment()
    processing.value = false
    if (data) {
      if (data.status == 'active') await auth.getMe()
      emit('success')
      emit('update:modelValue', false)
    } else {
      throw new Error('Synchronization failed')
    }
  } catch {
    ui.showError('An error occurred processing your payment. Please try again later.')
  } finally {
    loading.value = false
  }
}

async function cancelPayment() {
  await subscription.cancelPendingSubscription({ confirmation: 'CANCEL' })
  emit('update:modelValue', false)
  await subscription.listSubscriptions()
}

function destroyPaymentElement() {
  paymentElement?.destroy()
  paymentElement = null
  elements = null
  stripe = null
  loading.value = false
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
