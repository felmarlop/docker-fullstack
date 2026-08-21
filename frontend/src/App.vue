<template>
  <v-app>
    <AppHeader />

    <AppDrawer v-if="auth.isAuthenticated && navigation" :items="navigation" />

    <v-main class="app-main">
      <AppSnackbar />

      <div class="app-content">
        <RouterView />
      </div>

      <AppFooter />
    </v-main>
  </v-app>
</template>

<script setup>
import { RouterView } from 'vue-router'

import AppSnackbar from '@/components/common/AppSnackbar.vue'
import AppDrawer from '@/components/layout/AppDrawer.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import navigation from '@/navigation/account'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.app-main {
  display: flex;
  flex-direction: column;

  min-height: calc(100vh - var(--v-layout-top));
}

.app-content {
  flex: 1;
}
</style>
