<template>
  <v-container class="py-10" fluid>
    <div class="mx-auto account-content">
      <div class="mb-8">
        <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis">Subscription & Billing</h1>
      </div>

      <v-card variant="outlined" class="account-card mb-8">
        <div class="pa-6 border-b" :class="currentTier.bgClass">
          <div class="d-flex align-center justify-space-between w-100 mb-4">
            <v-avatar :color="currentTier.avatarColor" size="48" class="elevation-1">
              <v-icon :icon="currentTier.icon" :color="currentTier.iconColor" size="26" />
            </v-avatar>
            <v-chip :class="currentTier.badgeClass" :color="currentTier.badgeColor" variant="flat" size="small">
              {{ currentTier.badgeText }}
            </v-chip>
          </div>

          <div>
            <div v-if="!isPending" class="font-weight-bold text-uppercase text-medium-emphasis mb-1">Current Plan</div>
            <h2 class="text-h5 font-weight-bold text-high-emphasis tracking-tight">
              {{ currentTier.title }}
            </h2>
            <p class="text-body-2 text-medium-emphasis mt-1 mb-0">
              {{ currentTier.description }}
            </p>
          </div>
        </div>

        <v-card-text class="pa-6">
          <div class="d-flex align-center justify-space-between text-body-2">
            <div>
              <span class="text-medium-emphasis d-block mb-1">Billing Cycle</span>
              <span class="font-weight-bold text-high-emphasis">
                {{ currentTier.billing }}
              </span>
            </div>

            <v-btn
              v-if="plan !== 'free'"
              prepend-icon="mdi-close-circle-outline"
              variant="outlined"
              color="default"
              size="small"
              class="px-4"
              @click="cancelDialog = true"
            >
              Cancel Subscription
            </v-btn>
          </div>
        </v-card-text>
      </v-card>

      <div v-if="plan !== 'plus-lifetime'" class="d-flex flex-column ga-6">
        <v-card
          v-for="p in Object.values(subscriptionStore.plans)"
          :key="p.id"
          variant="outlined"
          class="account-card"
          :class="`${p.id}-gradient-bg`"
        >
          <v-card-item class="pa-6 border-b">
            <div class="d-flex align-center justify-space-between w-100">
              <div>
                <v-card-title class="text-h6 font-weight-bold"> Upgrade to {{ p.name }} </v-card-title>
                <v-card-subtitle class="text-body-2 text-medium-emphasis">
                  {{ p.description }}
                </v-card-subtitle>
              </div>

              <div class="text-right">
                <span class="text-h5 font-weight-bold text-high-emphasis">{{ `${p.amount} ${p.currency}` }}</span>
                <span v-if="p.is_lifetime" class="text-medium-emphasis"> / once</span>
              </div>
            </div>
          </v-card-item>

          <v-card-text v-if="proFeatures.length" class="pa-6 border-b bg-grey-lighten-5">
            <label class="font-weight-bold text-uppercase text-medium-emphasis mb-3 d-block"> Included in Pro </label>

            <v-list density="compact" bg-color="transparent" class="pa-0">
              <v-list-item v-for="(feature, index) in proFeatures" :key="index" class="px-0 mb-2">
                <template #prepend>
                  <v-icon icon="mdi-check-circle-outline" color="primary" size="18" class="mr-3" />
                </template>
                <v-list-item-title class="text-body-2 text-high-emphasis">
                  {{ feature }}
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>

          <v-card-text class="pa-6">
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center text-medium-emphasis">
                <v-icon icon="mdi-shield-check-outline" size="16" class="mr-1" />
                Lifetime access unlocked
              </div>

              <v-btn
                elevation="0"
                size="large"
                prepend-icon="mdi-lightning-bolt-outline"
                :color="PLAN_COLORS[p.id].button"
                :loading="loadingTier === p.id"
                :disabled="!!loadingTier"
                @click="handleUpgrade(p.id)"
              >
                Upgrade to <b class="mx-1">{{ p.name }}</b> — {{ `${p.amount} ${p.currency}` }}
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </div>

      <v-dialog v-model="cancelDialog" max-width="480">
        <v-card variant="outlined" class="danger-card bg-surface">
          <v-card-item class="pa-6 border-b">
            <v-card-title class="text-h6 font-weight-bold text-error"> Cancel Subscription? </v-card-title>
          </v-card-item>
          <v-card-text class="pa-6 text-body-2 text-medium-emphasis">
            <span>
              Are you sure you want to cancel your <strong>{{ plan.toUpperCase() }}</strong> plan? Your account will
              immediately revert to the Free Tier, and you will lose access to premium tier limits.
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
                :disabled="subscriptionStore.loading"
              />
              <v-divider class="mb-6" />
              <div class="d-flex justify-end ga-3">
                <v-btn
                  variant="text"
                  color="default"
                  size="large"
                  class="px-6 font-weight-bold"
                  :disabled="subscriptionStore.loading"
                  @click="closeDialog"
                >
                  Keep Plan
                </v-btn>
                <v-btn
                  type="submit"
                  color="error"
                  elevation="0"
                  size="large"
                  prepend-icon="mdi-close-circle-outline"
                  :loading="subscriptionStore.loading"
                  :disabled="cancelDisabled"
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
import { computed, onMounted, reactive, ref } from 'vue'
import * as subscriptionApi from '@/core/api/modules/subscription'
import { useSubscriptionStore } from '@/stores/subscription'
import { useUiStore } from '@/stores/ui'

const PLAN_COLORS = {
  'plus-lifetime': {
    button: 'primary',
  },
  'pro-lifetime': {
    button: 'accent',
  },
}

const subscriptionStore = useSubscriptionStore()
const ui = useUiStore()

const loadingTier = ref(null)
const cancelDialog = ref(false)

const proFeatures = []
const plusFeatures = []

const formRef = ref(null)
const form = reactive({
  confirmation: '',
})

const plan = computed(() => {
  return subscriptionStore.currentSubscription?.plan || 'free'
})

const isPending = computed(() => {
  return subscriptionStore.currentSubscription?.status || 'pending'
})

const currentTier = computed(() => {
  switch (plan.value) {
    case 'plus-lifetime':
      return {
        title: isPending.value ? 'Plus Access (Pending)' : 'Lifetime Plus Access',
        description: isPending.value
          ? 'Payment verification in progress. Full access will unlock shortly.'
          : 'Highest performance tier with maximum speed and priority access.',
        billing: isPending.value ? 'Processing...' : 'One-time (Lifetime)',
        bgClass: isPending.value ? 'pending-gradient-bg' : 'plus-gradient-bg',
        avatarColor: isPending.value ? 'warning' : 'primary',
        icon: isPending.value ? 'mdi-clock-outline' : 'mdi-lightning-bolt-outline',
        iconColor: 'white',
        badgeText: isPending.value ? 'PENDING APPROVAL' : 'PLUS MEMBER',
        badgeClass: isPending.value ? 'pending-badge font-weight-bold px-3' : 'plus-badge font-weight-bold px-3',
        badgeColor: undefined,
      }
    case 'pro-lifetime':
      return {
        title: isPending.value ? 'Pro Access (Pending)' : 'Lifetime Pro Access',
        description: isPending.value
          ? 'Payment verification in progress. Full access will unlock shortly.'
          : 'Expanded capabilities and workspace features.',
        billing: isPending.value ? 'Processing...' : 'One-time (Lifetime)',
        bgClass: isPending.value ? 'pending-gradient-bg' : 'pro-gradient-bg',
        buttonColor: 'accent',
        avatarColor: isPending.value ? 'warning' : 'accent',
        icon: isPending.value ? 'mdi-clock-outline' : 'mdi-star-outline',
        iconColor: 'white',
        badgeText: isPending.value ? 'PENDING APPROVAL' : 'PRO MEMBER',
        badgeClass: isPending.value ? 'pending-badge font-weight-bold px-3' : 'pro-badge font-weight-bold px-3',
        badgeColor: undefined,
      }
    default:
      return {
        title: 'Basic Account',
        description: 'Standard plan with core capabilities enabled.',
        billing: 'None',
        bgClass: 'basic-bg',
        buttonColor: 'primary',
        avatarColor: 'grey-lighten-3',
        icon: 'mdi-account-outline',
        iconColor: 'medium-emphasis',
        badgeText: 'FREE TIER',
        badgeClass: 'font-weight-bold',
        badgeColor: 'grey',
      }
  }
})

const cancelDisabled = computed(() => {
  return form.confirmation != 'CANCEL'
})

async function handleUpgrade(tier) {
  if (!subscriptionStore.plans[tier]) {
    ui.showError('Plan not available. Please try again later.')
    return
  }

  loadingTier.value = tier

  try {
    const { data } = await subscriptionApi.create({ plan: subscriptionStore.plans[tier] })
    subscriptionStore.setSubscription(data?.subscription || null)
    ui.showSuccess(`Congratulations! You have upgraded to ${tier.toUpperCase()}.`)
  } catch {
    ui.showError('Payment processing failed. Please try again later.')
  } finally {
    loadingTier.value = null
  }
}

async function handleCancelSubscription() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  await subscriptionStore.cancelSubscription({ confirmation: form.confirmation })
  this.closeDialog()
}

function closeDialog() {
  cancelDialog.value = false
  form.confirmation = ''
}

onMounted(async () => {
  if (!subscriptionStore.plans.length) {
    await subscriptionStore.getPlans()
  }
  /*if (Object.keys(subscriptionStore.plans).length) {
    await subscriptionStore.listSubscriptions()
  }*/
})
</script>
