<template>
  <v-container class="fill-height py-10 auth-content" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <email-sent-msg v-if="completed && form.email" action="reset your password" :email="form.email" />

        <v-card v-else variant="outlined" class="auth-card">
          <v-card-text class="pa-8">
            <div class="text-center mb-8">
              <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-1">Reset password</h1>
              <div class="mt-1">
                <AuthLink text="Remember your password?" action="Log in" to="/login" />
              </div>
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
                  v-model="form.email"
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
                prepend-icon="mdi-lock-reset"
                :loading="loading"
                :disabled="loading || !canSubmit"
                class="font-weight-bold"
              >
                Send Reset Link
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import AuthLink from '@/components/auth/AuthLink.vue'
import EmailSentMsg from '@/components/auth/EmailSentMsg.vue'
import * as rules from '@/helpers/validation'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const loading = ref(false)
const completed = ref(false)
const error = ref('')

const formRef = ref(null)

const form = reactive({
  email: '',
})

const canSubmit = computed(() => form.email.trim().length > 0)

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  completed.value = false
  error.value = ''

  try {
    await auth.forgotPassword(form)
    completed.value = true
  } catch (err) {
    let details = err.details ?? null
    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      error.value = Object.values(details)[0]?.[0] ?? ''
    } else {
      error.value = err.message ?? 'An unexpected error occurred. Please try again.'
    }
    if (err.code === 'account_not_activated') {
      router.push({ name: 'resend-activation', query: { email: form.email } })
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
