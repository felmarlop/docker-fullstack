<template>
  <v-snackbar
    v-model="ui.snackbar.show"
    :color="ui.snackbar.color"
    :timeout="env.snackbarTimeout"
    location="bottom end"
    max-width="360"
    rounded="lg"
    elevation="6"
  >
    <div class="d-flex align-center">
      <v-icon class="me-3" icon="mdi-alert-circle-outline" size="18" />

      <span class="text-body-2">
        {{ ui.snackbar.text }}
      </span>
    </div>

    <template #actions>
      <v-btn density="comfortable" icon="mdi-close" size="x-small" variant="text" @click="ui.hideSnackbar()" />
    </template>
  </v-snackbar>
</template>

<script setup>
import { useUiStore } from '@/stores/ui'
import env from '@/config/env'

const ui = useUiStore()
</script>
