<template>
  <v-main>
    <v-container class="fill-height">
      <v-row class="fill-height" justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <activate-account-msg v-if="inactive" />
          <v-card v-else rounded="lg" elevation="2">
            <v-card-text class="pa-8">
              <div class="d-flex mb-6">
                <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/login"> Back </v-btn>
              </div>

              <div class="text-center mb-8">
                <h1 class="text-h5 font-weight-bold">Reset password</h1>

                <AuthLink text="Remember your password?" action="Log in" to="/login" />
              </div>

              <v-alert v-if="error" class="mb-6" type="error" variant="tonal" density="comfortable">
                {{ error }}
              </v-alert>

              <v-form ref="formRef" @submit.prevent="submit">
                <v-text-field
                  v-model="form.email"
                  label="Email"
                  prepend-inner-icon="mdi-email-outline"
                  autocomplete="email"
                  variant="outlined"
                  :rules="[rules.required, rules.email]"
                  :disabled="loading"
                  class="mb-6"
                />

                <v-btn
                  type="submit"
                  color="primary"
                  block
                  prepend-icon="mdi-lock-reset"
                  :loading="loading"
                  :disabled="loading || !canSubmit"
                >
                  SEND RESET LINK
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'

import ActivateAccountMsg from '@/components/auth/ActivateAccountMsg.vue'
import AuthLink from '@/components/auth/AuthLink.vue'
import * as rules from '@/helpers/validation'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const loading = ref(false)
const error = ref('')
const inactive = ref(false)

const formRef = ref(null)

const form = reactive({
  email: '',
})

const canSubmit = computed(() => form.email.trim().length > 0)

async function submit() {
  const { valid } = await formRef.value.validate()

  if (!valid) {
    return
  }

  loading.value = true
  error.value = ''

  try {
    await auth.forgotPassword(form)
  } catch (err) {
    const defaultMessage = err.message ?? ''
    const firstError = Object.values(err.details ?? {})[0]?.[0]
    inactive.value = err.code === 'account_not_activated'
    error.value = firstError ?? defaultMessage
  } finally {
    loading.value = false
  }
}

watch(
  form,
  () => {
    error.value = ''
  },
  {
    deep: true,
  },
)
</script>
