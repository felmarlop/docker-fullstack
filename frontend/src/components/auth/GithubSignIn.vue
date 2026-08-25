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
        <v-img :src="gihtubIcon" width="18" height="18" class="mr-2" />
      </template>

      Continue with GitHub
    </v-btn>
  </div>
</template>

<script setup>
import { ref } from 'vue'

import env from '@/config/env'
import gihtubIcon from '@/assets/icons/github.svg'

const STORAGE_KEY = 'github:oauth:state'

const loading = ref(false)

async function showPrompt() {
  loading.value = true
  localStorage.setItem(STORAGE_KEY, generateState())

  const params = new URLSearchParams({
    client_id: env.githubClientId,
    redirect_uri: `${window.location.origin}/oauth/github/callback`,
    scope: 'user:email',
    state: localStorage.getItem(STORAGE_KEY),
  })

  window.location.href = `https://github.com/login/oauth/authorize?${params}`
}

function generateState() {
  const bytes = new Uint8Array(16)
  crypto.getRandomValues(bytes)
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('')
}
</script>
