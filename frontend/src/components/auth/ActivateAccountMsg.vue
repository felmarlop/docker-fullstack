<template>
  <v-card rounded="lg" elevation="2">
    <v-card-text class="pa-8">
      <div class="d-flex mb-6">
        <v-btn prepend-icon="mdi-chevron-left" variant="text" @click="emit('close')"> Back </v-btn>
      </div>

      <div class="text-center">
        <v-icon icon="mdi-email-alert-outline" color="primary" size="80" class="mb-6" />

        <h1 class="text-h5 font-weight-bold mb-3">Activate your account</h1>

        <p class="text-medium-emphasis mb-8">Please activate your account before continuing.</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
const emit = defineEmits(['close'])
</script>
