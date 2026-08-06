<template>
  <v-navigation-drawer
    v-model:rail="rail"
    app
    permanent
  >
    <v-list
      nav
      density="default"
      class="py-4"
    >
      <v-list-item
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        :prepend-icon="item.icon"
        :title="item.title"
        rounded="lg"
        class="mx-2 mb-1"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const rail = ref(false)
</script>

<style scoped>
:deep(.v-list-item-title) {
  font-weight: 400;
  font-size: 0.8rem;
  text-transform: uppercase;
  color: rgb(var(--v-theme-on-surface));
}
</style>
