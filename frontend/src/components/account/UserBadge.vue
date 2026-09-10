<template>
  <v-avatar
    v-if="subscriptionBadge"
    :size="badgeSize"
    :color="subscriptionBadge?.color"
    class="subscription-badge elevation-2"
  >
    <v-icon :icon="subscriptionBadge?.icon" :size="badgeIconSize" color="white" />
  </v-avatar>
</template>

<script setup>
import { computed } from 'vue'
import { PLAN_PROPS } from '@/config/stripe'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

defineProps({
  badgeSize: {
    type: Number,
    default: 35,
  },
  badgeIconSize: {
    type: Number,
    default: 22,
  },
})

const subscriptionBadge = computed(() => {
  if (auth.user?.subscription) {
    return PLAN_PROPS[auth.user.subscription.plan]
  }
  return null
})
</script>

<style scoped></style>
