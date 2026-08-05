<template>
  <v-main>
    <v-container class="fill-height">
      <v-row class="fill-height" justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <email-sent-msg v-if="completed && form.email" action="activate your account" :email="form.email" />
          <v-card v-else rounded="lg" elevation="2">
            <v-card-text class="pa-8">
              <div class="d-flex mb-6">
                <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/"> Back </v-btn>
              </div>

              <div class="text-center mb-8">
                <h1 class="text-h5 font-weight-bold">Sign up</h1>

                <AuthLink text="Already have an account?" action="Log in" to="/login" />
              </div>

              <v-alert v-if="error" class="mb-6" type="error" variant="tonal" density="comfortable">
                {{ error }}
              </v-alert>

              <v-form ref="formRef" @submit.prevent="submit">
                <v-text-field
                  v-model="form.username"
                  label="Username"
                  prepend-inner-icon="mdi-account-outline"
                  autocomplete="username"
                  variant="outlined"
                  :error-messages="detailErrors.username"
                  :rules="[rules.required]"
                  :disabled="loading"
                  class="mb-4"
                />

                <v-text-field
                  v-model="form.email"
                  label="Email"
                  prepend-inner-icon="mdi-email-outline"
                  autocomplete="email"
                  variant="outlined"
                  :error-messages="detailErrors.email"
                  :rules="[rules.required, rules.email]"
                  :disabled="loading"
                  class="mb-4"
                />

                <v-text-field
                  v-model="form.phone"
                  label="Phone (optional)"
                  prepend-inner-icon="mdi-phone-outline"
                  autocomplete="tel"
                  placeholder="+34 600 111 222"
                  variant="outlined"
                  :error-messages="detailErrors.phone"
                  :disabled="loading"
                  class="mb-4"
                />

                <v-text-field
                  v-model="form.password"
                  label="Password"
                  :type="showPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock-outline"
                  :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  autocomplete="new-password"
                  variant="outlined"
                  :error-messages="detailErrors.password"
                  :rules="[rules.required]"
                  :disabled="loading"
                  class="mb-6"
                  @click:append-inner="showPassword = !showPassword"
                />

                <v-btn
                  type="submit"
                  color="primary"
                  block
                  prepend-icon="mdi-account-plus-outline"
                  :loading="loading"
                  :disabled="loading || !canSubmit"
                >
                  SIGN UP
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
  return form.username.trim().length > 0 && form.email.trim().length > 0 && form.password.trim().length > 0
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
    delete details.code
    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      detailErrors.value = details
    } else {
      error.value = err.message ?? ''
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
  {
    deep: true,
  },
)
</script>
