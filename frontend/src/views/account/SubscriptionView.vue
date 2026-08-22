<template>
  <v-container class="py-10" fluid>
    <div class="mx-auto account-content">
      <div class="mb-8">
        <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis">Subscription & Billing</h1>
      </div>

      <v-card variant="outlined" class="account-card mb-8">
        <div class="pa-6 border-b" :class="isPro ? 'pro-gradient-bg' : 'basic-bg'">
          <div class="d-flex align-center justify-space-between w-100 mb-4">
            <v-avatar :color="isPro ? 'primary' : 'grey-lighten-3'" size="48" class="elevation-1">
              <v-icon
                :icon="isPro ? 'mdi-crown-outline' : 'mdi-account-outline'"
                :color="isPro ? 'white' : 'medium-emphasis'"
                size="26"
              />
            </v-avatar>

            <v-chip
              :class="isPro ? 'pro-badge font-weight-bold px-3' : 'font-weight-bold'"
              :color="isPro ? undefined : 'grey'"
              variant="flat"
              size="small"
            >
              {{ isPro ? 'PRO MEMBER' : 'FREE TIER' }}
            </v-chip>
          </div>

          <div>
            <div class="text-caption font-weight-bold text-uppercase text-medium-emphasis mb-1">Current Plan</div>
            <h2 class="text-h5 font-weight-bold text-high-emphasis tracking-tight">
              {{ isPro ? 'Lifetime Pro Access' : 'Basic Account' }}
            </h2>
            <p class="text-body-2 text-medium-emphasis mt-1 mb-0">
              {{
                isPro
                  ? 'Full unrestricted access to all feature suites.'
                  : 'Standard plan with core capabilities enabled.'
              }}
            </p>
          </div>
        </div>

        <v-card-text class="pa-6">
          <div class="d-flex align-center justify-space-between text-body-2">
            <span class="text-medium-emphasis">Billing Cycle</span>
            <span class="font-weight-bold text-high-emphasis">{{ isPro ? 'One-time (Lifetime)' : 'None' }}</span>
          </div>
        </v-card-text>
      </v-card>

      <v-card v-if="!isPro" variant="outlined" class="account-card">
        <v-card-item class="pa-6 border-b">
          <div class="d-flex align-center justify-space-between w-100">
            <div>
              <v-card-title class="text-h6 font-weight-bold"> Upgrade to Pro </v-card-title>
              <v-card-subtitle class="text-body-2 text-medium-emphasis">
                Unlock all premium features with a one-time lifetime payment.
              </v-card-subtitle>
            </div>

            <div class="text-right">
              <span class="text-h5 font-weight-bold text-high-emphasis">$29</span>
              <span class="text-caption text-medium-emphasis"> / once</span>
            </div>
          </div>
        </v-card-item>

        <v-card-text v-if="proFeatures.length" class="pa-6 border-b bg-grey-lighten-5">
          <label class="text-caption font-weight-bold text-uppercase text-medium-emphasis mb-3 d-block">
            Included in Pro Tier
          </label>

          <v-list density="compact" bg-color="transparent" class="pa-0">
            <v-list-item v-for="(feature, index) in proFeatures" :key="index" class="px-0 mb-2">
              <template #prepend>
                <v-icon icon="mdi-check-circle-outline" color="success" size="18" class="mr-3" />
              </template>
              <v-list-item-title class="text-body-2 text-high-emphasis">
                {{ feature }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-text class="pa-6">
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            density="comfortable"
            icon="mdi-alert-circle-outline"
            class="mb-6 rounded-lg"
          >
            {{ error }}
          </v-alert>

          <div class="d-flex align-center justify-space-between">
            <div class="d-flex align-center text-caption text-medium-emphasis">
              <v-icon icon="mdi-shield-check-outline" size="16" class="mr-1" />
              Secure 256-bit encrypted checkout
            </div>

            <v-btn
              color="primary"
              elevation="0"
              size="large"
              prepend-icon="mdi-credit-card-outline"
              :loading="loading"
              class="px-6 font-weight-bold"
              @click="handleUpgrade"
            >
              Upgrade Now — $29
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

const isPro = ref(false)
const loading = ref(false)
const error = ref('')

const proFeatures = []

async function handleUpgrade() {
  loading.value = true
  error.value = ''

  try {
    await new Promise((resolve) => setTimeout(resolve, 1500))
    isPro.value = true
    ui.showSuccess('Congratulations! You have successfully upgraded to Pro.')
  } catch {
    error.value = 'Payment processing failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
