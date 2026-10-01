<template>
  <v-app :class="{ 'app-layout': auth.isAuthenticated }">
    <AppHeader />

    <AppDrawer v-if="auth.isAuthenticated && accountNavigation" :items="menuItems" />

    <v-main class="app-main" :class="{ expanded: smAndDown }">
      <AppSnackbar />

      <div class="app-content">
        <RouterView />
      </div>

      <AppFooter />
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import { RouterView, useRoute } from 'vue-router'

import AppSnackbar from '@/components/common/AppSnackbar.vue'
import AppDrawer from '@/components/layout/AppDrawer.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import accountNavigation from '@/navigation/account'
import hubNavigation from '@/navigation/hub'

import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const { smAndDown } = useDisplay()
const auth = useAuthStore()
const route = useRoute()

if (smAndDown.value) useUiStore().drawerRail = true

const menuItems = computed(() => {
  return route.path.includes('/account') ? accountNavigation : hubNavigation
})
</script>

<style scoped>
.app-main {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - var(--v-layout-top));
  &.expanded {
    padding-left: 0px !important;
  }
}

.app-content {
  flex: 1;
}
</style>
