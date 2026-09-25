<template>
  <v-container fluid class="fill-height py-10">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" md="8" lg="6" class="mx-auto">
        <div class="text-center mb-8">
          <v-avatar color="primary-lighten-5" size="112" class="mb-6">
            <BrandLogo :size="70" animated />
          </v-avatar>

          <div
            class="text-md-headline-large text-headline-small font-weight-bold tracking-tight text-high-emphasis mb-2"
          >
            Docker Fullstack Boilerplate
          </div>

          <p class="text-body-1 text-medium-emphasis mx-auto" style="max-width: 520px">
            Ready-to-use development environment for modern Django REST Framework and Vue 3 applications.
          </p>
        </div>

        <div class="d-flex align-center my-6">
          <v-divider />
          <span class="mx-4 font-weight-bold text-uppercase text-medium-emphasis text-no-wrap">
            Backend API Health
          </span>
          <v-divider />
        </div>

        <v-card variant="outlined" class="api-response-card mx-auto mb-6" max-width="580">
          <template v-if="loading && ui.pingData" #loader>
            <v-progress-linear indeterminate color="primary" />
          </template>

          <v-fade-transition mode="out-in">
            <div
              v-if="loading && !ui.pingData"
              class="d-flex flex-column align-center justify-center"
              style="min-height: 180px"
            >
              <v-progress-circular indeterminate color="primary" size="32" class="mb-3" />
              <div class="text-medium-emphasis">Connecting to API...</div>
            </div>

            <div v-else key="content">
              <v-card-item class="py-2 border-b bg-surface-light">
                <div class="d-flex align-center justify-space-between w-100">
                  <div class="d-flex align-center">
                    <span class="text-primary font-weight-black mr-2">GET</span>
                    <span class="text-body-2 font-weight-bold text-medium-emphasis">/api/ping</span>
                  </div>

                  <v-chip :color="error ? 'error' : 'success'" variant="tonal" size="small" class="font-weight-bold">
                    <template #prepend>
                      <v-icon
                        :icon="error ? 'mdi-close-circle-outline' : 'mdi-check-circle-outline'"
                        size="16"
                        class="mr-1"
                      />
                    </template>
                    {{ error ? `${error.status} ${error.code}` : '200 OK' }}
                  </v-chip>
                </div>
              </v-card-item>

              <div class="terminal-body pa-4">
                <pre>{{ error ? formattedError : formattedResponse }}</pre>
              </div>
            </div>
          </v-fade-transition>
        </v-card>

        <div class="d-flex flex-column align-center gap-3 my-8">
          <div class="d-flex align-center ga-3 flex-wrap justify-center">
            <v-btn
              color="primary"
              elevation="0"
              prepend-icon="mdi-login"
              to="/login"
              size="large"
              rounded="lg"
              class="px-6 font-weight-bold"
            >
              Sign In
            </v-btn>

            <v-btn
              variant="outlined"
              prepend-icon="mdi-account-plus-outline"
              to="/register"
              size="large"
              rounded="lg"
              class="px-6 font-weight-semibold"
            >
              Register
            </v-btn>
          </div>
        </div>

        <div class="d-flex align-center my-6">
          <v-divider />
          <span class="mx-4 font-weight-bold text-uppercase text-medium-emphasis text-no-wrap">
            Developer Resources
          </span>
          <v-divider />
        </div>

        <div class="d-flex justify-center flex-wrap ga-3">
          <v-btn
            color="default"
            variant="outlined"
            href="/admin/"
            prepend-icon="mdi-shield-account-outline"
            class="font-weight-bold border-color-soft"
          >
            Django Admin
          </v-btn>

          <v-btn
            color="default"
            variant="outlined"
            href="/api/docs/"
            prepend-icon="mdi-api"
            class="font-weight-bold border-color-soft"
          >
            API Docs
          </v-btn>

          <v-btn
            color="default"
            variant="outlined"
            href="https://github.com/felmarlop/docker-fullstack#-docker-fullstack-boilerplate"
            prepend-icon="mdi-book-open-page-variant-outline"
            rel="noopener noreferrer"
            target="_blank"
            class="font-weight-bold border-color-soft"
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

import BrandLogo from '@/components/common/BrandLogo.vue'
import api from '@/core/api'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const loading = ref(true)
const error = ref(null)

const formattedResponse = computed(() => (ui.pingData ? JSON.stringify(ui.pingData, null, 2) : ''))

const formattedError = computed(() => {
  if (!error.value) return ''

  return JSON.stringify(
    {
      status: error.value.status || 0,
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
    ui.setPingData(data)
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.api-response-card {
  border-radius: 12px;
  overflow: hidden;
  border-color: rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}
</style>
