<template>
  <v-container class="fill-height py-10 auth-content" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card variant="outlined" class="auth-card">
          <template #loader>
            <v-progress-linear indeterminate color="primary" height="3" />
          </template>

          <v-card-text class="pa-8">
            <div class="text-center py-4">
              <v-avatar color="grey-lighten-4" size="60" class="mb-6">
                <v-img :src="githubIcon" width="60" height="60" alt="GitHub Logo" />
              </v-avatar>
              <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-2">Connecting to GitHub</h1>
              <p class="text-body-2 text-medium-emphasis mb-0">Please wait while we verify your credentials...</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import githubIcon from '@/assets/icons/github.svg'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const STORAGE_KEY = 'github:oauth:state'
const ERROR_MESSAGE = 'We could not log you in with GitHub. Please try again.'

const auth = useAuthStore()
const ui = useUiStore()
const router = useRouter()
const route = useRoute()

function showError(error) {
  let msg = error?.message ?? ERROR_MESSAGE
  if (error.details && error.details.non_field_errors.length) {
    msg = error.details.non_field_errors[0]
  }
  ui.showError(msg)
}

onMounted(async () => {
  const code = route.query.code
  const state = route.query.state
  try {
    if (state != localStorage.getItem(STORAGE_KEY) || !code) return showError()
    await auth.loginWithGithub(code)
    router.push('/')
  } catch (error) {
    router.push({ name: 'login' })
    showError(error)
  }
})
</script>
