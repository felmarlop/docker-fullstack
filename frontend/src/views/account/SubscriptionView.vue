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
            <div class="font-weight-bold text-uppercase text-medium-emphasis mb-1">Current Plan</div>
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
              v-if="userTier !== 'free'"
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

      <div v-if="userTier !== 'plus'" class="d-flex flex-column ga-6">
        <v-card v-if="userTier === 'free'" variant="outlined" class="account-card pro-gradient-bg">
          <v-card-item class="pa-6 border-b">
            <div class="d-flex align-center justify-space-between w-100">
              <div>
                <v-card-title class="text-h6 font-weight-bold"> Upgrade to Pro </v-card-title>
                <v-card-subtitle class="text-body-2 text-medium-emphasis">
                  Essential tools and expanded limits for active users.
                </v-card-subtitle>
              </div>

              <div class="text-right">
                <span class="text-h5 font-weight-bold text-high-emphasis">$19</span>
                <span class="text-medium-emphasis"> / once</span>
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
                256-bit encrypted checkout
              </div>

              <v-btn
                color="accent"
                elevation="0"
                size="large"
                prepend-icon="mdi-star-outline"
                :loading="loadingTier === 'pro'"
                :disabled="!!loadingTier"
                @click="handleUpgrade('pro')"
              >
                Upgrade to <b class="mx-1">Pro</b> — $19
              </v-btn>
            </div>
          </v-card-text>
        </v-card>

        <v-card variant="outlined" class="account-card plus-gradient-bg">
          <v-card-item class="pa-6 border-b">
            <div class="d-flex align-center justify-space-between w-100">
              <div>
                <v-card-title class="text-h6 font-weight-bold"> Upgrade to Plus </v-card-title>
                <v-card-subtitle class="text-body-2 text-medium-emphasis">
                  Maximum performance, unlimited capacity, and priority features.
                </v-card-subtitle>
              </div>

              <div class="text-right">
                <span class="text-h5 font-weight-bold text-high-emphasis">$49</span>
                <span class="text-medium-emphasis"> / once</span>
              </div>
            </div>
          </v-card-item>

          <v-card-text v-if="plusFeatures.length" class="pa-6 border-b bg-grey-lighten-5">
            <label class="font-weight-bold text-uppercase text-medium-emphasis mb-3 d-block"> Included in Plus </label>

            <v-list density="compact" bg-color="transparent" class="pa-0">
              <v-list-item v-for="(feature, index) in plusFeatures" :key="index" class="px-0 mb-2">
                <template #prepend>
                  <v-icon icon="mdi-check-circle-outline" style="color: #7c3aed" size="18" class="mr-3" />
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
                color="primary"
                prepend-icon="mdi-lightning-bolt-outline"
                :loading="loadingTier === 'plus'"
                :disabled="!!loadingTier"
                @click="handleUpgrade('plus')"
              >
                Upgrade to <b class="mx-1">Plus</b> — $49
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
            Are you sure you want to cancel your <strong>{{ userTier.toUpperCase() }}</strong> plan? Your account will
            immediately revert to the Free Tier, and you will lose access to premium tier limits.
          </v-card-text>

          <v-card-actions class="pa-6 pt-0 d-flex justify-end ga-3">
            <v-btn variant="plain" :disabled="cancelling" @click="cancelDialog = false"> Keep Plan </v-btn>

            <v-btn color="error" elevation="0" :loading="cancelling" @click="handleCancelSubscription">
              Confirm Cancellation
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

// Tier state: 'free' | 'pro' | 'plus'
const userTier = ref('free')
const loadingTier = ref(null)
const cancelDialog = ref(false)
const cancelling = ref(false)

const proFeatures = []

const plusFeatures = []

const currentTier = computed(() => {
  switch (userTier.value) {
    case 'plus':
      return {
        title: 'Lifetime Plus Access',
        description: 'Highest performance tier with maximum speed and priority access.',
        billing: 'One-time (Lifetime)',
        bgClass: 'plus-gradient-bg',
        avatarColor: 'primary',
        icon: 'mdi-lightning-bolt-outline',
        iconColor: 'white',
        badgeText: 'PLUS MEMBER',
        badgeClass: 'plus-badge font-weight-bold px-3',
        badgeColor: undefined,
      }
    case 'pro':
      return {
        title: 'Lifetime Pro Access',
        description: 'Expanded capabilities and workspace features.',
        billing: 'One-time (Lifetime)',
        bgClass: 'pro-gradient-bg',
        avatarColor: 'accent',
        icon: 'mdi-star-outline',
        iconColor: 'white',
        badgeText: 'PRO MEMBER',
        badgeClass: 'pro-badge font-weight-bold px-3',
        badgeColor: undefined,
      }
    default:
      return {
        title: 'Basic Account',
        description: 'Standard plan with core capabilities enabled.',
        billing: 'None',
        bgClass: 'basic-bg',
        avatarColor: 'grey-lighten-3',
        icon: 'mdi-account-outline',
        iconColor: 'medium-emphasis',
        badgeText: 'FREE TIER',
        badgeClass: 'font-weight-bold',
        badgeColor: 'grey',
      }
  }
})

async function handleUpgrade(tier) {
  loadingTier.value = tier

  try {
    await new Promise((resolve) => setTimeout(resolve, 1500))
    userTier.value = tier
    ui.showSuccess(`Congratulations! You have upgraded to ${tier.toUpperCase()}.`)
  } catch {
    ui.showError('Payment processing failed. Please try again.')
  } finally {
    loadingTier.value = null
  }
}

async function handleCancelSubscription() {
  cancelling.value = true

  try {
    await new Promise((resolve) => setTimeout(resolve, 1200))
    userTier.value = 'free'
    cancelDialog.value = false
    ui.showSuccess('Your subscription has been cancelled. Your account is now on the Free Tier.')
  } catch {
    ui.showError('Could not process cancellation. Please try again.')
  } finally {
    cancelling.value = false
  }
}
</script>
