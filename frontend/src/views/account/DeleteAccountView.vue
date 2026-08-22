<template>
  <v-container class="py-8" fluid>
    <div class="mx-auto account-content">
      <v-card rounded="lg" elevation="2" class="mb-10">
        <v-card-title class="d-flex align-center py-4 text-medium-emphasis">
          <span>Delete account</span>
        </v-card-title>

        <v-divider />

        <v-card-text>
          <v-alert v-if="error" class="mb-6" type="error" variant="tonal" density="comfortable">
            {{ error }}
          </v-alert>
          <v-alert v-else type="warning" variant="tonal" class="mb-6">
            <strong>This action cannot be undone.</strong><br />
            Your account and all associated data will be permanently deleted.
          </v-alert>

          <v-form ref="formRef" @submit.prevent="submit">
            <v-text-field
              v-model="form.password"
              label="Current password"
              :type="showPassword ? 'text' : 'password'"
              prepend-inner-icon="mdi-lock-outline"
              :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
              autocomplete="password"
              variant="outlined"
              :rules="[rules.required]"
              :error-messages="detailErrors.password"
              :disabled="loading"
              class="mb-4"
              @click:append-inner="showPassword = !showPassword"
            />

            <v-text-field
              v-model="form.confirmation"
              label="Type DELETE to confirm"
              variant="outlined"
              :rules="[rules.required]"
              :error-messages="detailErrors.confirmation"
              :disabled="loading"
            />

            <div class="d-flex ga-3 mt-2 justify-center">
              <v-btn
                type="submit"
                color="error"
                min-width="120"
                prepend-icon="mdi-delete-outline"
                :loading="loading"
                :disabled="disabled"
              >
                DELETE ACCOUNT
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

const disabled = computed(() => {
  return loading.value || !form.password || form.confirmation !== 'DELETE'
})

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''
  detailErrors.value = {}

  try {
    await auth.deleteAccount(form)

    router.push({ name: 'home' })
    ui.showSuccess('Your account has been successfully deleted.')
  } catch (err) {
    const details = err.details ?? null

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
