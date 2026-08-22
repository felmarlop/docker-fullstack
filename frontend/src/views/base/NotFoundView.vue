<template>
  <v-container class="fill-height py-10" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" class="text-center">
        <!-- Icon Bubble -->
        <v-avatar color="primary-lighten-5" size="112" class="mb-2">
          <v-icon color="primary" icon="mdi-magnify" size="56" class="magnify-icon" />
        </v-avatar>

        <h1 class="text-h2 font-weight-bold tracking-tight text-high-emphasis mt-6">404: Page not found</h1>

        <p class="text-body-1 text-medium-emphasis mt-3">Sorry, we couldn't find the page you're looking for.</p>

        <v-btn color="primary" elevation="0" prepend-icon="mdi-home-outline" to="/" class="mt-8 px-6 font-weight-bold">
          Back to Home
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.magnify-icon {
  animation: searchPulse 2.4s ease-in-out infinite;
}

@keyframes searchPulse {
  0%,
  100% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.12) rotate(12deg);
  }
}
</style>
