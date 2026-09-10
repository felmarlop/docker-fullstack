<template>
  <v-card variant="outlined" class="account-card">
    <v-progress-linear
      v-if="loadingTier == plan.id"
      indeterminate
      :color="planColor"
      height="3"
      class="position-absolute top-0 start-0 z-index-1"
    />
    <v-card-item class="pa-6 border-b" :class="`${plan.id}-gradient-bg`">
      <div class="d-flex align-center justify-space-between w-100">
        <div>
          <v-card-title class="text-h6 font-weight-bold"> Upgrade to {{ plan.name }} </v-card-title>
          <v-card-subtitle class="text-body-2 text-medium-emphasis">
            {{ plan.description }}
          </v-card-subtitle>
        </div>

        <div class="text-right">
          <span class="text-h5 font-weight-bold text-high-emphasis">{{ `${plan.amount} ${plan.currency}` }}</span>
          <span v-if="plan.is_lifetime" class="text-medium-emphasis"> / once</span>
        </div>
      </div>
    </v-card-item>

    <v-card-text v-if="plan.features && plan.features.length" class="pa-6 border-b bg-grey-lighten-5">
      <label class="font-weight-bold text-uppercase text-medium-emphasis mb-3 d-block">
        Included in {{ plan.name }}
      </label>

      <v-list density="compact" bg-color="transparent" class="pa-0">
        <v-list-item v-for="(feature, index) in plan.features" :key="index" class="px-0 mb-2">
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
          :prepend-icon="planIcon"
          :color="planColor"
          :disabled="loadingTier != null"
          @click="emit('upgrade', plan.id)"
        >
          Upgrade to <b class="mx-1">{{ plan.name }} — {{ `${plan.amount} ${plan.currency}` }}</b>
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { computed } from 'vue'
import { PLAN_PROPS } from '@/config/stripe'

const props = defineProps({
  plan: {
    type: Object,
    required: true,
  },
  loadingTier: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['upgrade'])

const planColor = computed(() => {
  return PLAN_PROPS[props.plan.id].color
})

const planIcon = computed(() => {
  return PLAN_PROPS[props.plan.id].icon
})
</script>
