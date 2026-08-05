<template>
  <v-container class="fill-height">
    <v-row class="fill-height" justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card rounded="lg" elevation="2">
          <v-card-text class="pa-8">
            <div v-if="!success" class="d-flex mb-6">
              <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/login"> Back </v-btn>
            </div>

            <template v-if="loading">
              <div class="text-center py-8">
                <v-progress-circular indeterminate color="primary" size="48" class="mb-6" />

                <h1 class="text-h5 font-weight-bold mb-3">Activating account</h1>

                <p class="text-medium-emphasis">Please wait while we activate your account.</p>
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
                  {{ success ? 'Account activated' : 'Activation failed' }}
                </h1>

                <p class="text-medium-emphasis mb-8">
                  {{ message }}
                </p>

                <v-btn v-if="success" color="primary" block prepend-icon="mdi-login" to="/login"> LOG IN </v-btn>
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
    message.value = 'Your account has been successfully activated.'
  } catch (err) {
    const defaultMessage = err.message ?? 'This activation link is invalid or has expired.'
    const firstError = Object.values(err.details ?? {})[0]?.[0]
    message.value = firstError ?? defaultMessage
  } finally {
    loading.value = false
  }
})
</script>
