<template>
  <v-main>
    <v-container class="fill-height">
      <v-row class="fill-height" justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card rounded="lg" elevation="2">
            <v-card-text class="pa-8">
              <div v-if="!success" class="d-flex mb-6">
                <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/login"> Back </v-btn>
              </div>

              <template v-if="success">
                <div class="text-center">
                  <v-icon icon="mdi-check-circle-outline" color="success" size="80" class="mb-6" />

                  <h1 class="text-h5 font-weight-bold mb-3">Password updated</h1>

                  <p class="text-medium-emphasis mb-8">Your password has been successfully updated.</p>

                  <v-btn color="primary" block prepend-icon="mdi-login" to="/login"> LOG IN </v-btn>
                </div>
              </template>

              <template v-else>
                <div class="text-center mb-8">
                  <h1 class="text-h5 font-weight-bold">Reset password</h1>

                  <p class="text-medium-emphasis mt-3">Enter your new password below.</p>
                </div>

                <v-alert v-if="error" class="mb-6" type="error" variant="tonal" density="comfortable">
                  {{ error }}
                </v-alert>

                <v-form ref="formRef" @submit.prevent="submit">
                  <v-text-field
                    v-model="form.password"
                    label="New password"
                    :type="showPassword ? 'text' : 'password'"
                    prepend-inner-icon="mdi-lock-outline"
                    :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                    autocomplete="new-password"
                    variant="outlined"
                    :rules="[rules.required]"
                    :disabled="loading"
                    class="mb-6"
                    @click:append-inner="showPassword = !showPassword"
                  />

                  <v-btn
                    type="submit"
                    color="primary"
                    block
                    prepend-icon="mdi-lock-reset"
                    :loading="loading"
                    :disabled="loading || !canSubmit"
                  >
                    CHANGE PASSWORD
                  </v-btn>
                </v-form>
              </template>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import * as authApi from '@/core/api/modules/auth'
import * as rules from '@/helpers/validation'

const route = useRoute()

const loading = ref(false)
const success = ref(false)
const error = ref('')
const showPassword = ref(false)

const formRef = ref(null)

const form = reactive({
  password: '',
})

const canSubmit = computed(() => {
  return form.password.trim().length > 0
})

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  success.value = false

  error.value = ''

  try {
    await authApi.resetPassword(route.params.uidb64, route.params.token, form.password)

    success.value = true
  } catch (err) {
    let details = err.details ?? null
    delete details.code
    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      error.value = Object.values(details)[0]?.[0] ?? ''
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
