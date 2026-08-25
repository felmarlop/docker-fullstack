<template>
  <v-container class="fill-height py-10 auth-content" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card variant="outlined" class="auth-card">
          <v-card-text class="pa-8">
            <div class="text-center mb-8">
              <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis">Sign in</h1>
              <div class="mt-1">
                <AuthLink text="Don't have an account?" action="Create one" to="/register" />
              </div>
            </div>
            <GoogleSignIn />
            <GithubSignIn />
            <div class="d-flex align-center mb-6">
              <v-divider />
              <span class="font-weight-bold text-uppercase text-medium-emphasis mx-4"> OR </span>
              <v-divider />
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
                  Email or Username
                </label>
                <v-text-field
                  v-model="form.username"
                  placeholder="Enter your email or username"
                  prepend-inner-icon="mdi-account-outline"
                  autocomplete="username"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :rules="[rules.required]"
                  :disabled="loading"
                />
              </div>

              <div class="mb-6">
                <label class="font-weight-bold text-uppercase text-medium-emphasis"> Password </label>
                <v-text-field
                  v-model="form.password"
                  placeholder="Enter your password"
                  :type="showPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock-outline"
                  :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  autocomplete="current-password"
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
                prepend-icon="mdi-login"
                :loading="loading"
                :disabled="loading || !canSubmit"
                class="font-weight-bold"
              >
                Log In
              </v-btn>
              <AuthLink action="Forgot password?" to="/reset-password" />
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
import GithubSignIn from '@/components/auth/GithubSignIn.vue'
import GoogleSignIn from '@/components/auth/GoogleSignIn.vue'
import * as rules from '@/helpers/validation'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const formRef = ref(null)
const form = reactive({
  username: '',
  password: '',
})

const canSubmit = computed(() => {
  return form.username.trim().length > 0 && form.password.trim().length > 0
})

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''

  try {
    await auth.login(form)
    router.push('/')
  } catch (err) {
    error.value = err.message ?? 'An error occurred while logging in.'

    if (err.code === 'account_not_activated') {
      const query = form.username.includes('@') ? { email: form.username } : {}
      router.push({ name: 'resend-activation', query: query })
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
