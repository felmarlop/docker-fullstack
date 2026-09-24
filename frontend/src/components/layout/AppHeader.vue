<template>
  <v-app-bar color="primary" elevation="1" class="d-flex px-2">
    <v-btn
      v-if="auth.isAuthenticated && smAndDown"
      variant="text"
      size="40"
      rounded="lg"
      class="me-1"
      @click="handleDrawerClick()"
    >
      <v-icon :icon="uiStore.drawerRail ? 'mdi-menu' : 'mdi-menu-open'" size="24" />
    </v-btn>

    <v-app-bar-title class="ms-0 ms-md-2">
      <RouterLink
        v-if="!smAndDown || !auth.isAuthenticated"
        to="/"
        class="header-link text-decoration-none ms-2 ms-md-0"
      >
        <v-avatar color="primary-lighten-5" size="38" class="me-3 brand-avatar">
          <BrandLogo :size="20" />
        </v-avatar>

        <span class="font-weight-bold text-title-medium text-md-title-large text-no-wrap">
          Docker Fullstack Boilerplate
        </span>
      </RouterLink>
    </v-app-bar-title>

    <v-spacer v-if="auth.isAuthenticated" />

    <v-menu
      v-if="auth.isAuthenticated"
      v-model="isUserMenuOpen"
      open-on-hover
      location="bottom end"
      :close-on-content-click="true"
      offset="8"
    >
      <template #activator="{ props }">
        <div v-bind="props" class="me-2 d-flex align-center cursor-pointer">
          <user-avatar :size="36" />
          <v-icon size="20" class="ms-1 opacity-80"> mdi-chevron-down </v-icon>
        </div>
      </template>

      <v-card min-width="260" rounded="lg" elevation="4">
        <div class="d-flex flex-column mx-2 my-5 align-center">
          <user-avatar :size="80" />
          <div class="mt-3 username">
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
import { ref, watch } from 'vue'

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

const isUserMenuOpen = ref(false)

function handleDrawerClick() {
  uiStore.toggleDrawerRail()
  isUserMenuOpen.value = !smAndDown.value
}

async function logout() {
  await auth.logout()
  router.push({ name: 'home' })
}

watch(isUserMenuOpen, (v) => {
  if (v && smAndDown.value) uiStore.drawerRail = true
})
</script>

<style scoped>
.header-link {
  display: inline-flex;
  align-items: center;
  color: inherit;
  text-decoration: none;
}

.brand-avatar {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.username {
  font-weight: 600;
}

.cursor-pointer {
  cursor: pointer;
}

.opacity-80 {
  opacity: 0.8;
}

:deep(.v-list-item__prepend) {
  margin-inline-end: 0 !important;
}
</style>
