<template>
  <v-container class="py-10" fluid>
    <div class="mx-auto account-content">
      <div class="mb-8">
        <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis">Subscription & Billing</h1>
      </div>

      <v-skeleton-loader v-if="firstLoading" class="mx-auto border" type="image, article" />
      <v-card v-else-if="!subscription.plans.length" variant="text" class="mb-8">
        <v-card-text class="pa-6 text-center">
          <v-avatar color="primary-lighten-5" size="112" class="mb-2">
            <v-icon color="primary" icon="mdi-magnify" size="56" class="magnify-icon" />
          </v-avatar>
          <h2 class="text-h2 tracking-tight text-high-emphasis mt-6">Subscription plans not found</h2>
          <p class="text-body-1 text-medium-emphasis mt-3">We couldn't retrieve the plans. Please try again later.</p>
        </v-card-text>
      </v-card>

      <SubscriptionCard
        v-if="subscription.plans.length && !firstLoading"
        :plan="currentPlan"
        :subscription="subscription.currentSubscription"
        @resume="handleResume()"
        @cancel="isPending ? cancelPendingSubscription() : openCancelDialog()"
      />

      <SubscriptionCard
        v-if="pendingPlan && pendingPlan.id != currentPlan.id && !firstLoading"
        :plan="pendingPlan"
        :subscription="subscription.pendingSubscription"
        :tier-props="PENDING_PROPS"
        @resume="handleResume()"
        @cancel="cancelPendingSubscription()"
      />

      <div v-if="plansToShow.length && !firstLoading" class="d-flex flex-column ga-6">
        <PlanCard
          v-for="p in plansToShow"
          :key="p.id"
          :plan="p"
          :loading-tier="loadingTier"
          @upgrade="handleUpgrade($event)"
        />
      </div>

      <PaymentDialog
        v-model="paymentDialog"
        :plan="currentPlan"
        :client-secret="clientSecret"
        @success="successMessage()"
      />

      <v-dialog v-model="cancelDialog" max-width="600">
        <v-card variant="outlined" class="danger-card bg-surface">
          <v-card-item class="pa-6 border-b">
            <template #prepend>
              <v-avatar color="error-lighten-5" size="44" class="mr-2">
                <v-icon icon="mdi-alert-octagon-outline" color="error" size="40" />
              </v-avatar>
            </template>
            <v-card-title class="text-h6 font-weight-bold text-error"> Cancel Subscription? </v-card-title>
          </v-card-item>
          <v-card-text class="pa-6 text-body-2 text-medium-emphasis">
            <span>
              Are you sure you want to cancel your <strong>{{ currentPlan.name.toUpperCase() }}</strong> plan? Your
              account will immediately revert to the Free Tier, and you will lose access to tier limits.
            </span>
            <v-form ref="formRef" class="mt-5" @submit.prevent="handleCancelSubscription()">
              <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block">
                Type <span class="font-weight-black text-high-emphasis">CANCEL</span> to confirm
              </label>
              <v-text-field
                v-model="form.confirmation"
                placeholder="CANCEL"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
                :disabled="subscription.loading"
              />
              <v-divider class="mb-6" />
              <div class="d-flex justify-end ga-3">
                <v-btn
                  variant="text"
                  color="default"
                  size="large"
                  class="px-6 font-weight-bold"
                  :disabled="subscription.cancelling"
                  @click="closeCancelDialog()"
                >
                  {{ isPending ? 'Close' : 'Keep Plan' }}
                </v-btn>
                <v-btn
                  type="submit"
                  color="error"
                  elevation="0"
                  size="large"
                  prepend-icon="mdi-close-circle-outline"
                  :loading="subscription.cancelling"
                  :disabled="form.confirmation != 'CANCEL'"
                  class="px-6 font-weight-bold"
                >
                  Confirm Cancellation
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import PaymentDialog from '@/components/payment/PaymentDialog.vue'
import PlanCard from '@/components/payment/PlanCard.vue'
import SubscriptionCard from '@/components/payment/SubscriptionCard.vue'
import * as subscriptionApi from '@/core/api/modules/subscription'
import { useAuthStore } from '@/stores/auth'
import { useSubscriptionStore } from '@/stores/subscription'
import { useUiStore } from '@/stores/ui'

const SYNCHRONIZING_TIMEOUT = 3000

const subscription = useSubscriptionStore()
const auth = useAuthStore()
const ui = useUiStore()

const firstLoading = ref(true)
const loadingTier = ref(null)
const clientSecret = ref(null)
const paymentDialog = ref(false)
const cancelDialog = ref(false)

let synchronizing = false
let syncInterval = null

const formRef = ref(null)
const form = reactive({
  confirmation: '',
})

const currentPlan = computed(() => {
  return (
    subscription.plans.find((p) => p.id == subscription.currentSubscription?.plan) || {
      id: 'free',
      title: 'Basic Account',
      name: 'free',
      description: 'Standard plan with core capabilities enabled.',
    }
  )
})

const pendingPlan = computed(() => {
  return subscription.plans.find((p) => p.id == subscription.pendingSubscription?.plan) || null
})

const isActive = computed(() => {
  if (!subscription.currentSubscription) return false
  return subscription.currentSubscription.status == 'active'
})

const isPending = computed(() => {
  if (!subscription.currentSubscription) return false
  return subscription.currentSubscription.status == 'pending'
})

const isProcessing = computed(() => {
  if (!subscription.currentSubscription) return false
  return subscription.currentSubscription.payment_status == 'processing'
})

const plansToShow = computed(() => {
  let toShow = []
  let _plans = subscription.plans.slice().reverse()
  for (let p of _plans) {
    if (currentPlan.value.id == p.id || pendingPlan.value?.id == p.id) break
    toShow.push(p)
  }
  return toShow.reverse()
})

async function handleUpgrade(tier) {
  const plan = subscription.plans.find((p) => p.id == tier)
  if (!plan) {
    ui.showError('Plan not available. Please try again later.')
    return
  }

  try {
    loadingTier.value = tier
    const { data } = await subscriptionApi.create({ plan: plan.id })
    clientSecret.value = data?.client_secret || null
    paymentDialog.value = true
  } catch {
    ui.showError('Payment processing failed. Please try again later.')
  } finally {
    loadingTier.value = null
    await subscription.listSubscriptions()
  }
}

async function handleResume() {
  const data = await subscription.resumePayment()
  if (data?.client_secret) {
    clientSecret.value = data?.client_secret || null
    paymentDialog.value = true
  }
}

async function handleCancelSubscription() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  await subscription.cancelCurrentSubscription({ confirmation: form.confirmation })
  await subscription.listSubscriptions()
  await auth.getMe()
  closeCancelDialog()
}

function handleProcessingPayment() {
  if (syncInterval) return
  syncInterval = setInterval(async () => {
    if (synchronizing) return
    try {
      synchronizing = true
      await subscription.syncPayment()
      if (isActive.value) {
        await auth.getMe()
        successMessage()
      }
    } finally {
      synchronizing = false
    }
  }, SYNCHRONIZING_TIMEOUT)
}

async function cancelPendingSubscription() {
  await subscription.cancelPendingSubscription({ confirmation: 'CANCEL' })
  await subscription.listSubscriptions()
}

function successMessage() {
  if (!isActive.value) return
  ui.showSuccess(`Congratulations! You now have ${currentPlan.value.name} access.`)
}

function openCancelDialog() {
  cancelDialog.value = true
}

function closeCancelDialog() {
  cancelDialog.value = false
  form.confirmation = ''
}

onMounted(async () => {
  firstLoading.value = true
  if (!subscription.plans.length) {
    await subscription.getPlans()
  }
  if (subscription.plans.length) {
    await subscription.listSubscriptions()
    await auth.getMe()
  }
  if (isProcessing.value) handleProcessingPayment()
  firstLoading.value = false
})

onBeforeUnmount(() => {
  clearInterval(syncInterval)
  syncInterval = null
})

watch(isProcessing, (v) => {
  if (v) {
    handleProcessingPayment()
  } else {
    clearInterval(syncInterval)
    syncInterval = null
  }
})
</script>

<style scoped>
.magnify-icon {
  animation: searchPulse 2.4s ease-in-out infinite;
}

@keyframes searchPulse {
  0%,
  100% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.12) rotate(12deg);
  }
}
</style>
