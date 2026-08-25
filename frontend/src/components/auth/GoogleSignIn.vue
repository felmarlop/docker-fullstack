<template>
  <div class="google-signin">
    <v-btn
      variant="outlined"
      block
      height="44"
      class="mb-6 font-weight-bold text-high-emphasis border-color-soft"
      :loading="loading"
      :disabled="loading"
      @click="showPrompt"
    >
      <template #prepend>
        <v-img :src="googleIcon" width="18" height="18" class="mr-2" />
      </template>

      Continue with Google
    </v-btn>
    <div ref="googleButton" class="google-button-container" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import env from '@/config/env'
import googleIcon from '@/assets/icons/google.svg'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const ERROR_MESSAGE = 'We could not log you in with Google. Please try again.'

const auth = useAuthStore()
const ui = useUiStore()
const router = useRouter()

const googleButton = ref(null)
const loading = ref(false)
const googleInitialized = ref(false)

function loadGoogleScript() {
  return new Promise((resolve, reject) => {
    if (window.google?.accounts?.id) {
      resolve()
      return
    }

    const script = document.createElement('script')

    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.onload = resolve
    script.onerror = reject

    document.head.appendChild(script)
  })
}

async function showPrompt() {
  try {
    loading.value = true
    await loadGoogleScript()
    if (!window.google?.accounts?.id || !googleButton.value) return showError()

    if (!googleInitialized.value) {
      window.google.accounts.id.initialize({
        client_id: env.googleClientId,
        callback: login,
      })

      window.google.accounts.id.renderButton(googleButton.value, {
        type: 'standard',
        theme: 'outline',
        size: 'large',
        text: 'continue_with',
        shape: 'rectangular',
        width: 400,
      })

      googleInitialized.value = true
    }

    const button = googleButton.value.querySelector('div[role="button"]')
    if (!button) return showError()
    button.click()
  } catch (error) {
    showError(error)
  } finally {
    loading.value = false
  }
}

async function login(response) {
  if (!response?.credential) return showError()

  loading.value = true

  try {
    await auth.loginWithGoogle(response.credential)
    router.push('/')
  } catch (err) {
    showError(err)
  } finally {
    loading.value = false
  }
}

function showError(error) {
  loading.value = false
  let msg = error?.message ?? ERROR_MESSAGE
  if (error.details && error.details.non_field_errors.length) {
    msg = error.details.non_field_errors[0]
  }
  ui.showError(msg)
}
</script>

<style scoped>
.google-button-container {
  position: absolute;
  visibility: hidden;
  width: 1px;
  height: 1px;
  pointer-events: none;
}
</style>
