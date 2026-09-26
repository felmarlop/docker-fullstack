<template>
  <v-container class="py-10 py-md-14" fluid>
    <div class="mx-auto account-content">
      <div class="text-md-headline-large text-headline-small font-weight-bold tracking-tight text-high-emphasis mb-8">
        Subscription & Billing
      </div>

      <v-skeleton-loader v-if="firstLoading" class="mx-auto border" type="image, article" />
      <v-card v-else-if="!subscription.plans.length" variant="text" class="mb-8">
        <v-card-text class="pa-6 text-center">
          <v-avatar color="primary-lighten-5" size="112" class="mb-2">
            <v-icon color="primary" icon="mdi-magnify" size="56" class="magnify-icon" />
          </v-avatar>
          <div class="text-md-headline-large text-headline-small tracking-tight text-high-emphasis mt-6">
            Subscription plans not found
          </div>
          <p class="text-body-1 text-medium-emphasis mt-3">We couldn't retrieve the plans. Please try again later.</p>
        </v-card-text>
      </v-card>

      <SubscriptionCard
        v-if="subscription.plans.length && !firstLoading"
        :plan="currentPlan"
        :subscription="subscription.currentSubscription"
        @resume="handleResume($event)"
        @cancel="isPending ? cancelPendingSubscription() : openCancelDialog()"
      />

      <SubscriptionCard
        v-if="pendingPlan && pendingPlan.id != currentPlan.id && !firstLoading"
        :plan="pendingPlan"
        :subscription="subscription.pendingSubscription"
        @resume="handleResume($event)"
        @cancel="cancelPendingSubscription()"
      />

      <div v-if="plansToShow.length && !firstLoading" class="d-flex flex-column ga-6">
        <PlanCard
          v-for="p in plansToShow"
          :key="p.id"
          :plan="p"
          :loading-tier="loadingTier"
          @upgrade="openConfirmDialog($event)"
        />
      </div>

      <ConfirmSubscriptionDialog v-model="confirmDialog" :plan="selectedPlan" @upgrade="handleUpgrade($event)" />
      <CancelSubscriptionDialog v-model="cancelDialog" :plan="currentPlan" :is-pending="isPending" />

      <PaymentDialog
        v-model="paymentDialog"
        :plan="selectedPlan"
        :client-secret="clientSecret"
        @success="handleSuccess()"
      />
    </div>
  </v-container>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import CancelSubscriptionDialog from '@/components/payment/CancelSubscriptionDialog.vue'
import ConfirmSubscriptionDialog from '@/components/payment/ConfirmSubscriptionDialog.vue'
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
const selectedPlan = ref(null)
const clientSecret = ref(null)
const paymentDialog = ref(false)
const confirmDialog = ref(false)
const cancelDialog = ref(false)

let synchronizing = false
let intervalId = null

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

const isCanceled = computed(() => {
  if (!subscription.currentSubscription) return false
  return subscription.currentSubscription.payment_status == 'canceled'
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

async function handleUpgrade(plan) {
  confirmDialog.value = false
  if (!plan) {
    ui.showError('Plan not available. Please try again later.')
    return
  }

  try {
    loadingTier.value = plan.id
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

async function handleResume(tier) {
  const plan = subscription.plans.find((p) => p.id == tier)
  if (!plan) {
    ui.showError('Plan not available. Please try again later.')
    return
  }

  selectedPlan.value = plan

  const data = await subscription.resumePayment()
  if (data?.client_secret) {
    clientSecret.value = data?.client_secret || null
    paymentDialog.value = true
  }
}

function handleProcessingPayment() {
  if (intervalId || !isProcessing.value) return
  intervalId = setInterval(async () => {
    if (synchronizing) return
    try {
      synchronizing = true
      await subscription.listSubscriptions()
      if (isActive.value) {
        await handleSuccess()
        clearInterval(intervalId)
      } else if (isCanceled.value) {
        clearInterval(intervalId)
        ui.showError('Payment processing failed. Please try again later.')
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

async function handleSuccess() {
  await auth.getMe()
  ui.showSuccess(`Congratulations! You now have ${currentPlan.value.name} access.`)
}

function openConfirmDialog(tier) {
  const plan = subscription.plans.find((p) => p.id == tier)
  if (!plan) {
    ui.showError('Plan not available. Please try again later.')
    return
  }
  selectedPlan.value = plan
  confirmDialog.value = true
}

function openCancelDialog() {
  cancelDialog.value = true
}

onMounted(async () => {
  firstLoading.value = true
  if (!subscription.plans.length) {
    await subscription.getPlans()
  }
  if (subscription.plans.length) {
    await subscription.listSubscriptions()
    if (subscription.pendingSubscription) {
      // Try to synchronize the subscription directly with stripe
      await subscription.syncPendingPayment()
    }

    await auth.getMe()
  }
  handleProcessingPayment()
  firstLoading.value = false
})

onBeforeUnmount(() => {
  clearInterval(intervalId)
  intervalId = null
})

watch(isProcessing, (v) => {
  if (v) {
    handleProcessingPayment()
  } else {
    clearInterval(intervalId)
    intervalId = null
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
