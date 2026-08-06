<template>
  <v-container class="fill-height">
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" class="text-center">
        <v-icon color="grey-darken-1" icon="mdi-magnify" size="96" class="magnify-icon" />

        <h1 class="text-h2 font-weight-bold mt-6">404: Not found</h1>

        <p class="text-h6 text-medium-emphasis mt-4">There's nothing here.</p>

        <v-btn class="mt-10" color="primary" prepend-icon="mdi-home" to="/" variant="flat"> Back to Home </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.magnify-icon {
  animation: searchPulse 2.4s ease-in-out;
  z-index: 2;
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
