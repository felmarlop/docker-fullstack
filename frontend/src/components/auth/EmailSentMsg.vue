<template>
  <v-card variant="outlined" class="auth-card">
    <v-card-text class="pa-8">
      <div class="mb-6">
        <v-btn prepend-icon="mdi-arrow-left" variant="text" to="/login" class="px-0 font-weight-bold"> Back </v-btn>
      </div>

      <div class="text-center">
        <v-avatar color="primary-lighten-5" size="64" class="mb-6">
          <v-icon icon="mdi-email-check-outline" color="primary" size="32" />
        </v-avatar>

        <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mb-2">Check your email</h1>

        <p class="text-body-1 text-medium-emphasis mb-0">
          If an account exists for <strong class="text-high-emphasis">{{ email }}</strong
          >, you will receive an email shortly to {{ action }}.
        </p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  email: {
    type: String,
    required: true,
  },
  action: {
    type: String,
    required: true,
  },
})
</script>
