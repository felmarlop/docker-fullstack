<template>
  <v-container class="fill-height py-10 auth-content" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <email-sent-msg v-if="completed && form.email" action="activate your account" :email="form.email" />

        <v-card v-else variant="outlined" class="auth-card">
          <v-card-text class="pa-8">
            <div class="text-center mb-8">
              <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis">Create an account</h1>
              <div class="mt-1">
                <AuthLink text="Already have an account?" action="Log in" to="/login" />
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
              <div class="mb-4">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block">
                  Username <span class="font-weight-regular text-lowercase">(optional)</span>
                </label>
                <v-text-field
                  v-model="form.username"
                  autofocus
                  placeholder="Leave empty for auto-generated"
                  prepend-inner-icon="mdi-account-outline"
                  autocomplete="username"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :error-messages="detailErrors.username"
                  :disabled="loading"
                />
              </div>

              <div class="mb-4">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block"> Email </label>
                <v-text-field
                  v-model="form.email"
                  placeholder="name@example.com"
                  prepend-inner-icon="mdi-email-outline"
                  autocomplete="email"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :error-messages="detailErrors.email"
                  :rules="[rules.required, rules.email]"
                  :disabled="loading"
                />
              </div>

              <div class="mb-6">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block"> Password </label>
                <v-text-field
                  v-model="form.password"
                  placeholder="Create a strong password"
                  :type="showPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock-outline"
                  :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  autocomplete="new-password"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :error-messages="detailErrors.password"
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
                prepend-icon="mdi-account-plus-outline"
                :loading="loading"
                :disabled="loading || !canSubmit"
                class="font-weight-bold"
              >
                Create Account
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

import AuthLink from '@/components/auth/AuthLink.vue'
import EmailSentMsg from '@/components/auth/EmailSentMsg.vue'
import * as rules from '@/helpers/validation'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const loading = ref(false)
const completed = ref(false)
const error = ref('')
const detailErrors = ref({})
const showPassword = ref(false)

const formRef = ref(null)
const form = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
})

const canSubmit = computed(() => {
  return form.email.trim().length > 0 && form.password.trim().length > 0
})

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  completed.value = false

  error.value = ''
  detailErrors.value = {}

  try {
    await auth.register(form)
    completed.value = true
  } catch (err) {
    let details = err.details ?? null
    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      detailErrors.value = details
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
