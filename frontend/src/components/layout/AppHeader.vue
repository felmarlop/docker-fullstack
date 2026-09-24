<template>
  <v-app-bar color="primary" elevation="1" class="d-flex px-2">
    <v-btn
      v-if="auth.isAuthenticated && smAndDown"
      variant="text"
      size="44"
      rounded
      @click="uiStore.toggleDrawerRail()"
    >
      <v-icon :icon="uiStore.drawerRail ? 'mdi-menu' : 'mdi-menu-open'" size="28" />
    </v-btn>

    <v-app-bar-title class="ms-md-4 ms-2">
      <RouterLink to="/" class="header-link text-decoration-none font-weight-500 text-title-large">
        <v-avatar color="primary-lighten-5" size="50" class="me-4">
          <BrandLogo :size="25" />
        </v-avatar>
        <span>Docker Fullstack Boilerplate</span>
      </RouterLink>
    </v-app-bar-title>

    <v-spacer />

    <v-menu v-if="auth.isAuthenticated" open-on-hover location="bottom end" :close-on-content-click="true" offset="8">
      <template #activator="{ props }">
        <div v-bind="props" class="me-2">
          <user-avatar :size="40" />
          <v-icon size="20" style="opacity: 0.8"> mdi-chevron-down </v-icon>
        </div>
      </template>

      <v-card min-width="260" rounded="lg" elevation="4">
        <div class="d-flex flex-column mx-2 my-5 align-center">
          <user-avatar :size="100" />
          <div class="mt-4 username">
            {{ auth.user?.username }}
          </div>
        </div>

        <v-list density="comfortable" nav class="px-2 pt-0">
          <v-list-item
            v-for="item in headerMenu"
            :key="item.title"
            :to="item.to"
            rounded="lg"
            color="primary"
            class="my-0"
          >
            <template #prepend>
              <v-icon :icon="item.icon" size="20" class="mr-5" />
            </template>
            <v-list-item-title class="text-body-2 font-weight-medium">
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
          <v-divider class="my-1" />
          <v-list-item rounded="lg" @click="logout">
            <template #prepend>
              <v-icon icon="mdi-logout" size="20" class="mr-5" />
            </template>
            <v-list-item-title class="text-body-2 font-weight-medium"> Log out </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
import { useDisplay } from 'vuetify'
import { useRouter } from 'vue-router'

import BrandLogo from '@/components/common/BrandLogo.vue'
import UserAvatar from '@/components/account/UserAvatar.vue'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

import headerMenu from '@/navigation/header-menu'

const { smAndDown } = useDisplay()

const auth = useAuthStore()
const router = useRouter()
const uiStore = useUiStore()

async function logout() {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.header-link {
  display: flex;
  align-items: center;
  color: inherit;
  text-decoration: none;
}

.username {
  font-weight: 600;
}

:deep(.v-list-item__prepend) {
  margin-inline-end: 0 !important;
}
</style>
