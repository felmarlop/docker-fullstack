<template>
  <v-container fluid class="fill-height">
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" md="8" lg="6">
        <div class="text-center">
          <v-icon color="primary" icon="mdi-rocket-launch" size="96" />

          <h1 class="text-h2 font-weight-bold mt-6">Welcome</h1>

          <p class="text-h6 text-medium-emphasis mt-4">Your Vue 3 + Vite + Vuetify frontend is ready.</p>

          <v-chip v-if="formattedResponse" class="mt-6" color="success" prepend-icon="mdi-check-circle" variant="tonal">
            Backend connection successful
          </v-chip>
        </div>

        <v-card v-if="formattedResponse" class="api-response mx-auto mt-6" max-width="520" variant="tonal">
          <v-card-title class="d-flex align-center justify-space-between">
            <span>GET /api/ping</span>

            <v-chip color="success" size="small" variant="flat"> 200 OK </v-chip>
          </v-card-title>

          <v-divider />

          <pre>{{ formattedResponse }}</pre>
        </v-card>

        <v-alert v-else-if="error" border="start" class="mx-auto mt-6" max-width="520" type="error" variant="tonal">
          <template #title> GET /api/ping failed </template>

          {{ error.message }}
        </v-alert>

        <v-row class="my-10 justify-center">
          <v-col cols="12" class="text-center">
            <v-btn color="primary" min-width="180" prepend-icon="mdi-login" to="/login"> Login </v-btn>
          </v-col>

          <v-col cols="12" class="d-flex justify-center flex-wrap ga-4 mt-2">
            <v-btn
              color="secondary"
              href="/admin/"
              min-width="180"
              prepend-icon="mdi-shield-account"
              variant="outlined"
            >
              Django Admin
            </v-btn>

            <v-btn color="secondary" href="/api/docs/" min-width="180" prepend-icon="mdi-api" variant="outlined">
              API Docs
            </v-btn>

            <v-btn
              href="https://github.com/felmarlop/docker-fullstack#-docker-fullstack-boilerplate"
              min-width="180"
              prepend-icon="mdi-book-open-page-variant"
              rel="noopener noreferrer"
              target="_blank"
              variant="outlined"
            >
              Documentation
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import api from '@/core/api'

const response = ref(null)
const error = ref(null)

const formattedResponse = computed(() => (response.value ? JSON.stringify(response.value, null, 2) : ''))

onMounted(async () => {
  try {
    const { data } = await api.get('ping')
    response.value = data
  } catch (err) {
    error.value = err
  }
})
</script>

<style scoped>
.api-response {
  text-align: left;
}

.api-response pre {
  margin: 0;
  padding: 20px;

  overflow-x: auto;

  font-family: 'SF Mono', Monaco, Consolas, 'Liberation Mono', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  white-space: pre-wrap;
}
</style>
