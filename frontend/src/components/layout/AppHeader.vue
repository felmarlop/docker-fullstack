<template>
  <v-app-bar color="primary" elevation="1" class="px-2">
    <v-app-bar-title class="d-flex align-center ga-2">
      <v-icon icon="mdi-rocket-launch" class="me-4" />
      <span>Docker Fullstack Boilerplate</span>
    </v-app-bar-title>
    <v-spacer />

    <RouterLink
      v-if="auth.isAuthenticated"
      :to="{ name: 'profile' }"
      class="header-link text-white text-decoration-none font-weight-medium me-4"
    >
      <v-icon icon="mdi-account-circle" size="20" class="me-2" />
      <span class="text-uppercase">{{ auth.user?.username }}</span>
    </RouterLink>

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

  transition: opacity 0.2s ease;
}

.header-link:hover {
  opacity: 0.8;
}
</style>
