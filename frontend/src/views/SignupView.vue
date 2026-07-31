<template>
  <v-main>
    <v-container class="fill-height">
      <v-row class="fill-height" justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card rounded="lg" elevation="2">
            <v-card-text class="pa-8">
              <div class="d-flex mb-6">
                <v-btn prepend-icon="mdi-chevron-left" variant="text" to="/"> Back </v-btn>
              </div>

              <div class="text-center mb-8">
                <h1 class="text-h5 font-weight-bold">Sign up</h1>

                <AuthLink text="Already have an account?" action="Sign in" to="/login" />
              </div>

              <p class="text-center text-disabled">Not available</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import AuthLink from '@/components/auth/AuthLink.vue'
</script>
