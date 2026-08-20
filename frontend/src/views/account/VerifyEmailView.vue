<template>
  <v-container class="fill-height">
    <v-row class="fill-height" justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card rounded="lg" elevation="2">
          <v-card-text class="pa-8">
            <template v-if="loading">
              <div class="text-center py-8">
                <v-progress-circular indeterminate color="primary" size="48" class="mb-6" />
                <h1 class="text-h5 font-weight-bold mb-3">Verifying email</h1>
                <p class="text-medium-emphasis">Please wait while we verify your email.</p>
              </div>
            </template>

            <template v-else>
              <div class="text-center">
                <v-icon
                  :icon="success ? 'mdi-check-circle-outline' : 'mdi-close-circle-outline'"
                  :color="success ? 'success' : 'error'"
                  size="80"
                  class="mb-6"
                />

                <h1 class="text-h5 font-weight-bold mb-3">
                  {{ success ? 'Email verified' : 'Email verification failed' }}
                </h1>

                <p class="text-medium-emphasis mb-8">
                  {{ message }}
                </p>

                <v-btn
                  v-if="auth.isAuthenticated"
                  color="primary"
                  block
                  prepend-icon="mdi-shield-account-outline"
                  to="/account/security"
                >
                  GO TO ACCOUNT
                </v-btn>
                <v-btn v-else color="primary" block prepend-icon="mdi-login" to="/login"> LOG IN </v-btn>
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

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()

const loading = ref(true)
const success = ref(false)
const message = ref('')

onMounted(async () => {
  try {
    await auth.verifyEmail(route.params.uidb64, route.params.token)

    success.value = true
    message.value = 'Your email has been successfully verified.'
  } catch (err) {
    const defaultMessage = err.message ?? 'This verification link is invalid or has expired.'
    const firstError = Object.values(err.details ?? {})[0]?.[0]
    message.value = firstError ?? defaultMessage
  } finally {
    loading.value = false
  }
})
</script>
