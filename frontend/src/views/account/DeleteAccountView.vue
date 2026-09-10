<template>
  <v-container class="py-10" fluid>
    <div class="mx-auto account-content">
      <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis">Delete account</h1>

      <v-card variant="outlined" class="danger-card border-error">
        <v-card-item class="pa-6 border-b">
          <template #prepend>
            <v-avatar color="error-lighten-5" size="44" class="mr-2">
              <v-icon icon="mdi-alert-octagon-outline" color="error" size="40" />
            </v-avatar>
          </template>

          <v-card-title class="text-h6 font-weight-bold text-error"> Account deletion </v-card-title>
          <v-card-subtitle class="text-body-2 text-medium-emphasis">
            Permanently remove your account and all your data.
          </v-card-subtitle>
        </v-card-item>

        <v-card-text class="pa-6">
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
            <div v-if="usablePassword">
              <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block">
                Enter your current password
              </label>
              <div class="mb-4">
                <v-text-field
                  v-model="form.password"
                  placeholder="Password"
                  :type="showPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock-outline"
                  :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  autocomplete="current-password"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :rules="[rules.required]"
                  :error-messages="detailErrors.password"
                  :disabled="loading"
                  @click:append-inner="showPassword = !showPassword"
                />
              </div>
            </div>

            <div class="mb-6">
              <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block">
                Type <span class="font-weight-black text-high-emphasis">DELETE</span> to confirm
              </label>
              <v-text-field
                v-model="form.confirmation"
                placeholder="DELETE"
                variant="outlined"
                density="comfortable"
                hide-details="auto"
                :rules="[rules.required]"
                :error-messages="detailErrors.confirmation"
                :disabled="loading"
              />
            </div>

            <v-divider class="mb-6" />

            <div class="d-flex justify-end ga-3">
              <v-btn
                variant="text"
                color="default"
                size="large"
                class="px-6 font-weight-bold"
                :disabled="loading"
                @click="router.back()"
              >
                Cancel
              </v-btn>

              <v-btn
                type="submit"
                color="error"
                elevation="0"
                size="large"
                prepend-icon="mdi-delete-forever-outline"
                :loading="loading"
                :disabled="disabled"
                class="px-6 font-weight-bold"
              >
                Delete Account
              </v-btn>
            </div>
          </v-form>
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

import * as rules from '@/helpers/validation'

const auth = useAuthStore()
const router = useRouter()
const ui = useUiStore()

const loading = ref(false)
const showPassword = ref(false)
const error = ref('')
const detailErrors = ref({})

const formRef = ref(null)

const form = reactive({
  password: '',
  confirmation: '',
})

const usablePassword = computed(() => {
  return auth.user?.has_usable_password ?? false
})

const disabled = computed(() => {
  const check = loading.value || form.confirmation !== 'DELETE'
  return usablePassword.value ? check || !form.password : check
})

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''
  detailErrors.value = {}

  try {
    await auth.deleteAccount(form)

    router.push({ name: 'login' })
    ui.showSuccess('Your account has been successfully deleted.')
  } catch (err) {
    const details = err.details ?? null

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
    detailErrors.value = {}
  },
  {
    deep: true,
  },
)
</script>

<style scoped>
.account-content {
  max-width: 640px;
}
</style>
