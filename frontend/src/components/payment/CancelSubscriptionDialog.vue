<template>
  <v-dialog :model-value="modelValue" max-width="600">
    <v-card variant="outlined" class="danger-card bg-surface">
      <v-card-item class="pa-6 border-b">
        <template #prepend>
          <v-avatar color="error-lighten-5" size="44" class="mr-2">
            <v-icon icon="mdi-alert-octagon-outline" color="error" size="40" />
          </v-avatar>
        </template>
        <v-card-title class="font-weight-bold text-error"> Cancel Subscription? </v-card-title>
      </v-card-item>
      <v-card-text class="pa-6 text-body-2 text-medium-emphasis">
        <span>
          Are you sure you want to cancel your <strong>{{ currentPlan.name.toUpperCase() }}</strong> plan? Your account
          will immediately revert to the Free Tier, and you will lose access to tier limits.
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
</template>
<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useSubscriptionStore } from '@/stores/subscription'

const auth = useAuthStore()
const subscription = useSubscriptionStore()

const emit = defineEmits(['update:modelValue'])

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const formRef = ref(null)
const form = reactive({
  confirmation: '',
})

async function handleCancelSubscription() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  await subscription.cancelCurrentSubscription({ confirmation: form.confirmation })
  await subscription.listSubscriptions()
  await auth.getMe()
  closeCancelDialog()
}

function closeCancelDialog() {
  emit('update:modelValue', false)
  form.confirmation = ''
}
</script>
