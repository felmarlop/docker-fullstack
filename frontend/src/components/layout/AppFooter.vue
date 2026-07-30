<template>
  <v-footer border style="max-height: 100px">
    <v-container fluid>
      <div class="d-flex align-center justify-space-between flex-wrap ga-2">
        <span class="text-caption text-medium-emphasis"> Docker Fullstack Boilerplate © {{ currentYear }} </span>

        <div class="d-flex align-center ga-1">
          <v-btn
            href="https://github.com/felmarlop/docker-fullstack"
            icon="mdi-github"
            rel="noopener noreferrer"
            target="_blank"
            variant="text"
          />

          <v-btn
            href="https://github.com/felmarlop/docker-fullstack#-docker-fullstack-boilerplate"
            prepend-icon="mdi-book-open-page-variant"
            rel="noopener noreferrer"
            target="_blank"
            size="small"
            variant="text"
          >
            Documentation
          </v-btn>
        </div>
      </div>
    </v-container>
  </v-footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>
