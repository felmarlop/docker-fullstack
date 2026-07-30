<template>
  <v-app>
    <v-app-bar color="primary" elevation="1">
      <v-app-bar-title>Docker Fullstack Boilerplate</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container class="fill-height">
        <v-row class="fill-height" align="center" justify="center">
          <v-col cols="12" md="8" lg="6">
            <div class="text-center">
              <v-icon color="primary" icon="mdi-rocket-launch" size="96" />

              <h1 class="text-h2 font-weight-bold mt-6">Welcome</h1>

              <p class="text-h6 text-medium-emphasis mt-4">Your Vue 3 + Vite + Vuetify frontend is ready.</p>

              <div class="d-flex justify-center ga-4 mt-10">
                <v-btn color="primary" prepend-icon="mdi-login"> Login </v-btn>

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
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup></script>

<style scoped></style>
