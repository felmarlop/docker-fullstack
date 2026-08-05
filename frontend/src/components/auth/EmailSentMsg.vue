<template>
  <v-card rounded="lg" elevation="2">
    <v-card-text class="pa-8">
      <div class="d-flex mb-6">
        <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/login"> Back </v-btn>
      </div>

      <div class="text-center">
        <v-icon icon="mdi-email-check-outline" color="primary" size="80" class="mb-6" />

        <h1 class="text-h5 font-weight-bold mb-3">Check your email</h1>

        <p class="text-medium-emphasis mb-8">
          If an account exists for
          <strong>{{ email }}</strong
          >, you'll receive email shortly to {{ action }}.
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
