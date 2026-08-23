<template>
  <v-footer class="app-footer">
    <div class="footer-content">
      <span class="text-medium-emphasis"> © {{ currentYear }} Docker Fullstack Boilerplate </span>

      <div class="d-flex align-center ga-1">
        <v-btn
          icon="mdi-github"
          href="https://github.com/felmarlop/docker-fullstack"
          target="_blank"
          rel="noopener noreferrer"
          variant="text"
          density="comfortable"
        />

        <v-btn
          prepend-icon="mdi-book-open-page-variant"
          href="https://github.com/felmarlop/docker-fullstack#-docker-fullstack-boilerplate"
          target="_blank"
          rel="noopener noreferrer"
          variant="text"
          density="comfortable"
        >
          Documentation
        </v-btn>
      </div>
    </div>
  </v-footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>
