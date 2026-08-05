<template>
  <v-container class="fill-height">
    <v-row class="fill-height" justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <email-sent-msg v-if="completed && email" action="activate your account" :email="email" />
        <v-card v-else rounded="lg" elevation="2">
          <v-card-text class="pa-8">
            <div class="d-flex mb-6">
              <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/login"> Back </v-btn>
            </div>

            <div class="text-center mb-8">
              <v-icon icon="mdi-email-alert-outline" color="primary" size="80" class="mb-6" />

              <h1 class="text-h5 font-weight-bold mb-3">Activate your account</h1>

              <p class="text-medium-emphasis">
                Enter the email address associated with your account to receive a new activation email.
              </p>
            </div>

            <v-alert v-if="error" class="mb-6" type="error" variant="tonal" density="comfortable">
              {{ error }}
            </v-alert>

            <v-form ref="formRef" @submit.prevent="submit">
              <v-text-field
                v-model="email"
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
                prepend-icon="mdi-email-fast-outline"
                :loading="loading"
                :disabled="loading || !email.trim()"
              >
                RESEND ACTIVATION EMAIL
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
      error.value = err.message ?? ''
    }
  } finally {
    loading.value = false
  }
}
</script>
