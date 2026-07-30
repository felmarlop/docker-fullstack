<template>
  <v-main>
    <v-app-bar color="primary" elevation="1">
      <v-app-bar-title>Docker Fullstack Boilerplate</v-app-bar-title>
    </v-app-bar>

    <v-container class="fill-height">
      <v-row align="center" class="fill-height" justify="center">
        <v-col cols="12" lg="6" md="8">
          <div class="text-center">
            <v-icon color="primary" icon="mdi-rocket-launch" size="96" />

            <h1 class="text-h2 font-weight-bold mt-6">Welcome</h1>

            <p class="text-h6 text-medium-emphasis mt-4">Your Vue 3 + Vite + Vuetify frontend is ready.</p>

            <v-chip
              v-if="formattedResponse"
              color="success"
              prepend-icon="mdi-check-circle"
              variant="tonal"
              class="mt-6"
            >
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
          <div class="d-flex justify-center ga-4 mt-10">
            <v-btn color="primary" prepend-icon="mdi-login" to="/login"> Login </v-btn>

            <v-btn
              href="https://github.com/felmarlop/docker-fullstack#-docker-fullstack-boilerplate"
              prepend-icon="mdi-book-open-page-variant"
              rel="noopener noreferrer"
              target="_blank"
              variant="outlined"
            >
              Documentation
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import api from '@/core/api'

const response = ref(null)

const formattedResponse = computed(() => (response.value ? JSON.stringify(response.value, null, 2) : ''))

onMounted(async () => {
  const { data } = await api.get('ping')
  response.value = data
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
