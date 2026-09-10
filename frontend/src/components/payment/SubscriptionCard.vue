<template>
  <v-card variant="outlined" class="account-card mb-8">
    <v-progress-linear
      v-if="isProcessing || subscriptionStore.loadingSubscription == subscription?.id"
      indeterminate
      :color="avatarColor"
      height="3"
      class="position-absolute top-0 start-0 z-index-1"
    />
    <div class="pa-6 border-b" :class="bgClass">
      <div class="d-flex align-center justify-space-between w-100 mb-4">
        <v-avatar :color="avatarColor" size="48" class="elevation-1">
          <v-icon :icon="badgeIcon" :color="badgeColor" size="26" />
        </v-avatar>
        <v-chip
          class="text-uppercase font-weight-bold px-3"
          :class="badgeClass"
          :color="isFree ? 'grey' : ''"
          variant="flat"
          size="small"
        >
          {{ badgeText }}
        </v-chip>
      </div>

      <div>
        <div v-if="!isPending" class="font-weight-bold text-uppercase text-medium-emphasis mb-1">Current Plan</div>
        <h2 class="text-h5 font-weight-bold text-high-emphasis tracking-tight">
          {{ isPending ? `${plan.title} (Pending)` : plan.title }}
        </h2>
        <p class="text-body-2 text-medium-emphasis mt-1 mb-0">
          {{ isPending ? PENDING_DESCRIPTION : isProcessing ? PROCESSING_DESCRIPTION : plan.description }}
        </p>
      </div>
    </div>

    <v-card-text class="pa-6">
      <div class="d-flex align-center justify-space-between text-body-2">
        <div v-if="plan.billing">
          <span class="text-medium-emphasis d-block mb-1">Billing Cycle</span>
          <span class="font-weight-bold text-high-emphasis">
            {{ isPending ? 'None' : isProcessing ? 'Processing...' : plan.billing }}
          </span>
        </div>
        <div v-else>
          <span class="text-medium-emphasis d-block mb-1">No Billing Cycle</span>
        </div>
        <div>
          <v-btn
            v-if="isPending"
            prepend-icon="mdi-credit-card-outline"
            variant="outlined"
            color="primary"
            size="small"
            class="px-4 me-4"
            :disabled="subscriptionStore.loadingSubscription == subscription?.id"
            @click="emit('resume')"
          >
            Continue payment
          </v-btn>
          <v-btn
            v-if="!isFree"
            prepend-icon="mdi-close-circle-outline"
            variant="outlined"
            color="default"
            size="small"
            class="px-4"
            :disabled="isProcessing || subscriptionStore.loadingSubscription == subscription?.id"
            @click="emit('cancel')"
          >
            {{ isPending ? 'Cancel' : 'Cancel Subscription' }}
          </v-btn>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { computed } from 'vue'
import { PLAN_PROPS } from '@/config/stripe'
import { useSubscriptionStore } from '@/stores/subscription'

const PENDING_DESCRIPTION = 'Complete your payment to activate your subscription.'
const PROCESSING_DESCRIPTION = 'Your payment is being processed. Access will unlock shortly.'

const subscriptionStore = useSubscriptionStore()

const props = defineProps({
  plan: {
    type: Object,
    required: true,
  },
  subscription: {
    type: Object,
    default: () => {
      return null
    },
  },
})

const isFree = computed(() => {
  return props.plan.id === 'free'
})

const isPending = computed(() => {
  if (!props.subscription) return false
  return props.subscription.status == 'pending'
})

const isProcessing = computed(() => {
  if (!props.subscription) return false
  return props.subscription.payment_status == 'processing'
})

const bgClass = computed(() => {
  return isPending.value ? 'pending-gradient-bg' : `${props.plan.id}-bg`
})

const avatarColor = computed(() => {
  if (isFree.value) return 'grey-lighten-3'
  return isPending.value ? 'warning' : PLAN_PROPS[props.plan.id].color
})

const badgeIcon = computed(() => {
  if (isFree.value) return 'mdi-account-outline'
  return isPending.value || isProcessing.value ? 'mdi-clock-outline' : PLAN_PROPS[props.plan.id].icon
})

const badgeColor = computed(() => {
  return isFree.value ? 'medium-emphasis' : 'white'
})

const badgeText = computed(() => {
  if (isFree.value) return 'free tier'
  return isPending.value ? 'pending payment' : isProcessing.value ? 'processing...' : `${props.plan.name} member`
})

const badgeClass = computed(() => {
  return isPending.value ? 'pending-badge' : PLAN_PROPS[props.plan.id]?.class
})

const emit = defineEmits(['resume', 'cancel'])
</script>
