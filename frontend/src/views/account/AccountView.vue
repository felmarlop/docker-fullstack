<template>
  <v-container class="py-8" fluid>
    <div class="mx-auto account-content">
      <div class="text-center mb-8">
        <v-avatar color="primary" size="180">
          <v-img
            v-if="auth.user?.username"
            :src="`https://i.pravatar.cc/180?u=${auth.user.username}`"
            :alt="auth.user.username"
          >
            <!-- Placeholder slot for loading and error states -->
            <template #placeholder>
              <!-- ADD THESE CLASSES to center the initial within the v-img -->
              <v-row class="fill-height ma-0" align="center" justify="center">
                <h1 class="font-weight-light text-white">
                  {{ auth.user.username[0].toUpperCase() }}
                </h1>
              </v-row>
            </template>
          </v-img>

          <!-- Absolute Fallback if no user exists -->
          <v-row v-else class="fill-height ma-0" align="center" justify="center">
            <h1 class="text-h3 font-weight-light">?</h1>
          </v-row>
        </v-avatar>

        <h1 class="text-h4 font-weight-bold mt-4">
          {{ auth.user?.username }}
        </h1>

        <p class="text-medium-emphasis">Personal information</p>
      </div>

      <v-card rounded="lg" elevation="2">
        <v-list lines="two">
          <v-list-item prepend-icon="mdi-account-outline" title="Username" :subtitle="auth.user?.username" />

          <v-divider />

          <v-list-item prepend-icon="mdi-email-outline" title="Email" :subtitle="auth.user?.email" />

          <v-divider />

          <v-list-item
            prepend-icon="mdi-shield-account-outline"
            title="Administrator"
            :subtitle="auth.user?.is_staff ? 'Yes' : 'No'"
          />

          <v-divider />

          <v-list-item
            prepend-icon="mdi-crown-outline"
            title="Superuser"
            :subtitle="auth.user?.is_superuser ? 'Yes' : 'No'"
          />
        </v-list>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.account-content {
  max-width: 760px;
}
</style>
