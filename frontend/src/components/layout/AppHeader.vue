<template>
  <v-app-bar color="primary" elevation="1" class="px-2">
    <v-app-bar-title>
      <RouterLink to="/" class="header-link text-decoration-none">
        <v-icon icon="mdi-rocket-launch" class="me-4" />

        <span>Docker Fullstack Boilerplate</span>
      </RouterLink>
    </v-app-bar-title>

    <v-spacer />

    <v-btn v-if="auth.isAuthenticated" :to="{ name: 'account-profile' }" icon="mdi-account-circle" variant="text" />

    <v-btn v-if="auth.isAuthenticated" icon="mdi-logout" variant="text" @click="logout" />
  </v-app-bar>
</template>

<script setup>
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function logout() {
  await auth.logout()
  router.push({ name: 'home' })
}
</script>

<style scoped>
.header-link {
  display: flex;
  align-items: center;

  color: inherit;
  text-decoration: none;
}
</style>
