<template>
  <v-app>
    <AppHeader />

    <v-main>
      <AppSnackbar />
      <RouterView />
    </v-main>

    <AppFooter />
  </v-app>
</template>

<script setup>
import { RouterView } from 'vue-router'

import AppFooter from '@/components/layout/AppFooter.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSnackbar from '@/components/common/AppSnackbar.vue'
</script>
