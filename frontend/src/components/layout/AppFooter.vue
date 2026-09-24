<template>
  <v-footer class="app-footer">
    <div class="footer-content ms-md-4">
      <span class="text-medium-emphasis text-md-body-medium text-body-small">
        © {{ currentYear }} Docker Fullstack Boilerplate
      </span>

      <div class="d-flex align-center">
        <v-btn
          icon="mdi-github"
          href="https://github.com/felmarlop/docker-fullstack"
          target="_blank"
          rel="noopener noreferrer"
          variant="text"
          density="comfortable"
        />

        <v-btn
          href="https://github.com/felmarlop/docker-fullstack#-docker-fullstack-boilerplate"
          target="_blank"
          rel="noopener noreferrer"
          variant="text"
          density="comfortable"
          :icon="smAndDown"
          rounded="lg"
        >
          <v-icon icon="mdi-book-open-page-variant" :class="{ 'mr-2': !smAndDown }" />
          <span v-if="!smAndDown">Documentation</span>
        </v-btn>
      </div>
    </div>
  </v-footer>
</template>

<script setup>
import { useDisplay } from 'vuetify'

const { smAndDown } = useDisplay()
const currentYear = new Date().getFullYear()
</script>
