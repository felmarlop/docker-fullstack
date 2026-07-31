<template>
  <v-main>
    <v-container class="fill-height">
      <v-row class="fill-height" justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card rounded="lg" elevation="2">
            <v-card-text class="pa-8">
              <div class="d-flex mb-6">
                <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/"> Back </v-btn>
              </div>

              <div class="text-center mb-8">
                <h1 class="text-h5 font-weight-bold">Log in</h1>

                <AuthLink text="Don't have an account?" action="Create one" to="/signup" />
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
                  :rules="[rules.required]"
                  :disabled="loading"
                  class="mb-4"
                />

                <v-text-field
                  v-model="form.password"
                  label="Password"
                  type="password"
                  prepend-inner-icon="mdi-lock-outline"
                  autocomplete="current-password"
                  variant="outlined"
                  :rules="[rules.required]"
                  :disabled="loading"
                  class="mb-6"
                />

                <v-btn
                  type="submit"
                  color="primary"
                  block
                  prepend-icon="mdi-login"
                  :loading="loading"
                  :disabled="loading || !canSubmit"
                >
                  LOG IN
                </v-btn>
                <AuthLink action="I forgot my password" to="/signup" />
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
import { useRouter } from 'vue-router'

import AuthLink from '@/components/auth/AuthLink.vue'
import * as rules from '@/helpers/validation'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const loading = ref(false)
const error = ref('')

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
    error.value = err.message ?? ''
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
