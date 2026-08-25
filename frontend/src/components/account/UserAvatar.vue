<template>
  <v-avatar :size="size" class="user-avatar">
    <v-img v-if="auth.user?.username" :src="auth.user?.avatar_url" :alt="auth.user.username">
      <template #placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <h1 class="font-weight-bold text-primary" :style="`font-size: ${size / 3}px`">
            {{ auth.user.username[0].toUpperCase() }}
          </h1>
        </v-row>
      </template>
    </v-img>
  </v-avatar>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

defineProps({
  size: {
    type: Number,
    default: 40,
  },
})
</script>

<style scoped>
.user-avatar {
  border: 1px solid rgb(var(--v-theme-primary));
  background-color: rgb(var(--v-theme-background)) !important;
}
</style>
