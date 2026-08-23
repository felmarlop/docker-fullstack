<template>
  <v-container class="fill-height py-10 auth-content" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <email-sent-msg v-if="completed && email" action="activate your account" :email="email" />

        <v-card v-else variant="outlined" class="auth-card">
          <v-card-text class="pa-8">
            <div class="mb-6">
              <v-btn prepend-icon="mdi-arrow-left" variant="text" to="/login" class="px-0 font-weight-bold">
                Back
              </v-btn>
            </div>

            <div class="text-center mb-8">
              <v-avatar color="primary-lighten-5" size="64" class="mb-4">
                <v-icon icon="mdi-email-alert-outline" color="primary" size="32" />
              </v-avatar>

              <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-2">Activate your account</h1>

              <p class="text-body-2 text-medium-emphasis">
                Enter the email address associated with your account to receive a new activation link.
              </p>
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
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block"> Email </label>
                <v-text-field
                  v-model="email"
                  autofocus
                  placeholder="name@example.com"
                  prepend-inner-icon="mdi-email-outline"
                  autocomplete="email"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :rules="[rules.required, rules.email]"
                  :disabled="loading"
                />
              </div>

              <v-btn
                type="submit"
                color="primary"
                block
                elevation="0"
                size="large"
                prepend-icon="mdi-email-fast-outline"
                :loading="loading"
                :disabled="loading || !email.trim()"
                class="font-weight-bold"
              >
                Resend Activation Email
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

import EmailSentMsg from '@/components/auth/EmailSentMsg.vue'

import * as authApi from '@/core/api/modules/auth'
import * as rules from '@/helpers/validation'

const route = useRoute()

const loading = ref(false)
const completed = ref(false)
const error = ref('')
const email = ref(route.query.email || '')
const formRef = ref(null)

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  completed.value = false
  error.value = ''

  try {
    await authApi.resendActivationEmail({ email: email.value })

    completed.value = true
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
</script>
