<template>
  <v-container fluid class="fill-height">
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" md="8" lg="6">
        <div class="text-center">
          <v-icon icon="mdi-rocket-launch" class="me-4 text-primary" size="120" />

          <h1 class="text-h3 font-weight-bold mt-4">Docker Fullstack Boilerplate</h1>

          <p class="text-h6 text-medium-emphasis mt-3">
            Ready-to-use development environment for modern Django and Vue applications.
          </p>
        </div>

        <div class="d-flex align-center my-6">
          <v-divider />

          <span class="mx-4 text-caption text-medium-emphasis text-no-wrap"> Backend Status </span>

          <v-divider />
        </div>

        <v-card v-if="formattedResponse || error" class="api-response mx-auto" max-width="580" variant="tonal">
          <v-card-title class="d-flex align-center justify-space-between">
            <span>GET /api/ping</span>

            <v-chip :color="error ? 'error' : 'success'" prepend-icon="mdi-check-circle" size="small" variant="flat">
              {{ error ? `${error.status} ${error.code}` : '200 OK' }}
            </v-chip>
          </v-card-title>

          <v-divider />

          <pre>{{ error ? formattedError : formattedResponse }}</pre>
        </v-card>

        <div v-if="!auth.isAuthenticated" class="d-flex align-center my-6">
          <v-divider />

          <span class="mx-4 text-caption text-medium-emphasis text-no-wrap"> JWT Authentication </span>

          <v-divider />
        </div>

        <div v-if="!auth.isAuthenticated" class="text-center">
          <v-btn color="primary" min-width="240" prepend-icon="mdi-login" to="/login"> LOG IN </v-btn>
          <AuthLink text="Don't have an account?" action="Create one" to="/signup" />
        </div>

        <div class="d-flex align-center my-6">
          <v-divider />

          <span class="mx-4 text-caption text-medium-emphasis text-no-wrap"> Developer Resources </span>

          <v-divider />
        </div>

        <div class="d-flex justify-center flex-wrap ga-4 mb-6">
          <v-btn color="secondary" href="/admin/" min-width="180" prepend-icon="mdi-shield-account" variant="outlined">
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
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import { useAuthStore } from '@/stores/auth'
import AuthLink from '@/components/auth/AuthLink.vue'

import api from '@/core/api'

const auth = useAuthStore()
const response = ref(null)
const error = ref(null)

const formattedResponse = computed(() => (response.value ? JSON.stringify(response.value, null, 2) : ''))

const formattedError = computed(() => {
  if (!error.value) {
    return ''
  }

  return JSON.stringify(
    {
      status: error.value.status || '',
      code: error.value.code || '',
      message: error.value.message || '',
    },
    null,
    2,
  )
})

onMounted(async () => {
  try {
    const { data } = await api.get('ping', { notify: true })
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
