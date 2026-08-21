<template>
  <v-app-bar color="primary" elevation="1" class="px-2">
    <v-app-bar-title>
      <RouterLink to="/" class="header-link text-decoration-none">
        <v-icon icon="mdi-rocket-launch" class="me-4" />
        <span>Docker Fullstack Boilerplate</span>
      </RouterLink>
    </v-app-bar-title>

    <v-spacer />

    <v-menu v-if="auth.isAuthenticated" open-on-hover location="bottom end" :close-on-content-click="true" offset="8">
      <template #activator="{ props }">
        <div v-bind="props" class="me-2">
          <user-avatar :size="40" />
          <v-icon size="18" style="opacity: 0.8"> mdi-chevron-down </v-icon>
        </div>
      </template>

      <v-card min-width="260" rounded="lg" elevation="4">
        <div class="d-flex flex-column mx-2 my-5 align-center">
          <user-avatar :size="100" />
          <div class="mt-4 username">
            {{ auth.user?.username }}
          </div>
        </div>

        <v-list density="comfortable" nav>
          <template v-for="item in headerMenu" :key="item.title">
            <v-list-item :to="item.to" :prepend-icon="item.icon" class="mt-0">
              <v-list-item-title class="text-body-1 font-weight-bold ps-6 mt-1">
                {{ item.title }}
              </v-list-item-title>
            </v-list-item>
            <v-divider />
          </template>
          <v-list-item prepend-icon="mdi-logout" class="mt-0" @click="logout">
            <v-list-item-title class="text-body-1 ps-6 mt-1"> Log out </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
import { useRouter } from 'vue-router'

import UserAvatar from '@/components/account/UserAvatar.vue'
import { useAuthStore } from '@/stores/auth'

import headerMenu from '@/navigation/header-menu'

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

.username {
  font-weight: 600;
}

:deep(.v-list-item) {
  border-radius: 0;
}

:deep(.v-list-item-title) {
  font-size: 0.85rem;
  font-weight: 500;
  min-height: 20px !important;
}
</style>
