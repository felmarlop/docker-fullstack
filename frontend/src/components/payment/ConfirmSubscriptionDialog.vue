<template>
  <v-dialog :model-value="modelValue" max-width="600" @update:model-value="emit('update:modelValue', $event)">
    <v-card variant="outlined" class="account-card bg-surface">
      <v-card-item class="pa-6 border-b" :class="`${plan.id}-gradient-bg`">
        <template #prepend>
          <v-avatar :color="avatarColor" size="44" class="mr-2">
            <v-icon :icon="badgeIcon" color="white" size="26" />
          </v-avatar>
        </template>
        <v-card-title class="font-weight-bold"> {{ plan.title }} </v-card-title>
        <v-card-subtitle class="text-body-2 text-medium-emphasis"> {{ plan.description }} </v-card-subtitle>
      </v-card-item>

      <v-card-text class="pa-6 text-body-2 text-medium-emphasis">
        <span>
          You are about to upgrade to the <strong>{{ plan.name.toUpperCase() }}</strong> plan. Review your selection
          below before proceeding to checkout.
        </span>

        <v-sheet rounded="lg" color="surface-light" class="pa-6 my-5 border text-center">
          <div class="text-h4 font-weight-black text-high-emphasis">
            {{ plan.amount }} {{ plan.currency.toUpperCase() }}
          </div>
          <div v-if="plan.is_lifetime" class="text-caption text-medium-emphasis mt-1">
            One-time payment • Lifetime access
          </div>
        </v-sheet>

        <v-sheet
          v-if="plan.features && plan.features.length"
          rounded="lg"
          color="surface-light"
          class="pa-4 my-5 border"
        >
          <label class="font-weight-bold text-uppercase text-medium-emphasis mb-2 d-block">
            Included in {{ plan.name }}
          </label>
          <v-list density="compact" bg-color="transparent" class="pa-0">
            <v-list-item v-for="(feature, index) in plan.features" :key="index" class="px-0 py-0 min-height-0">
              <template #prepend>
                <v-icon icon="mdi-check-circle-outline" color="primary" size="18" class="mr-2" />
              </template>
              <v-list-item-title class="text-body-2 text-high-emphasis">
                {{ feature }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-sheet>

        <div class="d-flex align-center justify-center text-medium-emphasis my-4">
          <v-icon icon="mdi-shield-check-outline" size="18" class="mr-2" color="primary" />
          <span>Encrypted & secure checkout</span>
        </div>

        <v-form ref="formRef" class="mt-5" @submit.prevent="emit('upgrade', plan)">
          <v-divider class="mb-6" />
          <div class="d-flex justify-end ga-3">
            <v-btn variant="text" color="default" size="large" class="px-6 font-weight-bold" @click="closeDialog()">
              Cancel
            </v-btn>
            <v-btn
              type="submit"
              elevation="0"
              size="large"
              class="px-6 text-white"
              prepend-icon="mdi-credit-card-outline"
              :color="planColor"
            >
              Proceed to Checkout
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { PLAN_PROPS } from '@/config/stripe'

const emit = defineEmits(['update:modelValue', 'upgrade'])

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  plan: {
    type: Object,
    required: false,
    default: () => {
      return null
    },
  },
})

const avatarColor = computed(() => {
  return PLAN_PROPS[props.plan.id]?.color || 'primary'
})

const badgeIcon = computed(() => {
  return PLAN_PROPS[props.plan.id]?.icon || 'mdi-star'
})

const planColor = computed(() => {
  return PLAN_PROPS[props.plan.id]?.color || 'primary'
})

function closeDialog() {
  emit('update:modelValue', false)
}
</script>
