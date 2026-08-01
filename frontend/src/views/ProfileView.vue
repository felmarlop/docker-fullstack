<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <div class="text-center mb-8">
          <v-avatar color="primary" size="100">
            <h1 class="text-h4 font-weight-light">
              {{ auth.user?.username[0].toUpperCase() }}
            </h1>
          </v-avatar>

          <h1 class="text-h4 font-weight-bold mt-4">
            {{ auth.user?.username }}
          </h1>

          <p class="text-medium-emphasis">Account information</p>
        </div>

        <v-card rounded="lg" elevation="2">
          <v-list lines="two">
            <v-list-item prepend-icon="mdi-account-outline" title="Username" :subtitle="auth.user?.username" />

            <v-divider />

            <v-list-item prepend-icon="mdi-email-outline" title="Email" :subtitle="auth.user?.email" />

            <v-divider />

            <v-list-item
              prepend-icon="mdi-shield-account-outline"
              title="Staff"
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
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>
