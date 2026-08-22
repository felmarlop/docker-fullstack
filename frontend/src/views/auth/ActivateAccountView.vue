<template>
  <v-container class="fill-height py-10 auth-content" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card variant="outlined" class="auth-card">
          <v-card-text class="pa-8">
            <div v-if="!success && !loading" class="mb-6">
              <v-btn
                prepend-icon="mdi-arrow-left"
                variant="text"
                size="small"
                to="/login"
                class="px-0 font-weight-bold"
              >
                Back
              </v-btn>
            </div>

            <template v-if="loading">
              <div class="text-center py-6">
                <v-progress-circular indeterminate color="primary" size="48" class="mb-6" />

                <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-2">Activating account</h1>

                <p class="text-body-1 text-medium-emphasis mb-0">
                  Please wait while we verify and activate your account...
                </p>
              </div>
            </template>

            <template v-else>
              <div class="text-center">
                <v-avatar :color="success ? 'success-lighten-5' : 'error-lighten-5'" size="64" class="mb-6">
                  <v-icon
                    :icon="success ? 'mdi-check-circle-outline' : 'mdi-alert-circle-outline'"
                    :color="success ? 'success' : 'error'"
                    size="32"
                  />
                </v-avatar>

                <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-2">
                  {{ success ? 'Account activated' : 'Activation failed' }}
                </h1>

                <p class="text-body-1 text-medium-emphasis mb-8">
                  {{ message }}
                </p>

                <v-btn
                  v-if="success"
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
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import * as authApi from '@/core/api/modules/auth'

const route = useRoute()

const loading = ref(true)
const success = ref(false)
const message = ref('')

onMounted(async () => {
  try {
    await authApi.activate(route.params.uidb64, route.params.token)

    success.value = true
    message.value = 'Your account has been successfully activated. You can now log in.'
  } catch (err) {
    const defaultMessage = err.message ?? 'This activation link is invalid or has expired.'
    const firstError = Object.values(err.details ?? {})[0]?.[0]
    message.value = firstError ?? defaultMessage
  } finally {
    loading.value = false
  }
})
</script>
