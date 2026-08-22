<template>
  <v-container class="fill-height py-10 auth-content" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card variant="outlined" class="auth-card">
          <v-card-text class="pa-8">
            <div v-if="!success" class="mb-6">
              <v-btn prepend-icon="mdi-arrow-left" variant="text" to="/login" class="px-0 font-weight-bold">
                Back
              </v-btn>
            </div>

            <template v-if="success">
              <div class="text-center">
                <v-avatar color="success-lighten-5" size="64" class="mb-6">
                  <v-icon icon="mdi-check-circle-outline" color="success" size="32" />
                </v-avatar>

                <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-2">Password updated</h1>

                <p class="text-body-1 text-medium-emphasis mb-8">
                  Your password has been successfully updated. You can now log in with your new credentials.
                </p>

                <v-btn
                  color="primary"
                  block
                  elevation="0"
                  size="large"
                  prepend-icon="mdi-login"
                  to="/login"
                  class="font-weight-bold"
                >
                  Log In
                </v-btn>
              </div>
            </template>

            <template v-else>
              <div class="text-center mb-8">
                <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-1">Set new password</h1>
                <p class="text-body-2 text-medium-emphasis mt-1">Please enter your new password below.</p>
              </div>

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

              <v-form ref="formRef" @submit.prevent="submit">
                <div class="mb-6">
                  <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block">
                    New Password
                  </label>
                  <v-text-field
                    v-model="form.password"
                    autofocus
                    placeholder="Enter your new password"
                    :type="showPassword ? 'text' : 'password'"
                    prepend-inner-icon="mdi-lock-outline"
                    :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                    autocomplete="new-password"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                    :rules="[rules.required]"
                    :disabled="loading"
                    @click:append-inner="showPassword = !showPassword"
                  />
                </div>

                <v-btn
                  type="submit"
                  color="primary"
                  block
                  elevation="0"
                  size="large"
                  prepend-icon="mdi-lock-reset"
                  :loading="loading"
                  :disabled="loading || !canSubmit"
                  class="font-weight-bold"
                >
                  Update Password
                </v-btn>
              </v-form>
            </template>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import * as authApi from '@/core/api/modules/auth'
import * as rules from '@/helpers/validation'

const route = useRoute()

const loading = ref(false)
const success = ref(false)
const error = ref('')
const showPassword = ref(false)

const formRef = ref(null)

const form = reactive({
  password: '',
})

const canSubmit = computed(() => {
  return form.password.trim().length > 0
})

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  success.value = false
  error.value = ''

  try {
    await authApi.resetPassword({
      uidb64: route.params.uidb64,
      token: route.params.token,
      new_password: form.password,
    })

    success.value = true
  } catch (err) {
    let details = err.details ?? null
    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      error.value = Object.values(details)[0]?.[0] ?? ''
    } else {
      error.value = err.message ?? 'An unexpected error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

watch(
  form,
  () => {
    error.value = ''
  },
  { deep: true },
)
</script>
