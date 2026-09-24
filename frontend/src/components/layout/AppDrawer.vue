<template>
  <v-navigation-drawer
    v-model:rail="uiStore.drawerRail"
    :rail-width="APP_DRAWER_RAIL_WIDTH"
    :permanent="!smAndDown || !uiStore.drawerRail"
    :temporary="smAndDown || uiStore.drawerRail"
    class="app-drawer border-e"
  >
    <v-overlay
      v-if="smAndDown"
      :model-value="!uiStore.drawerRail"
      class="drawer-overlay"
      scrim="#000000"
      :opacity="0.4"
      z-index="90"
      @click="uiStore.drawerRail = true"
    />

    <div class="drawer-header" :class="{ rail: uiStore.drawerRail }">
      <v-btn
        v-if="!smAndDown"
        :icon="uiStore.drawerRail ? 'mdi-chevron-right' : 'mdi-chevron-left'"
        variant="text"
        density="comfortable"
        color="primary"
        @click="uiStore.toggleDrawerRail()"
      />
    </div>

    <div class="d-flex flex-column align-center align-md-stretch">
      <v-avatar v-if="smAndDown" color="primary-lighten-5" size="60" class="brand-avatar text-center mt-2 mb-6">
        <BrandLogo :size="200" />
      </v-avatar>

      <v-list density="comfortable" nav class="px-2 py-0">
        <v-tooltip
          v-for="item in items"
          :key="item.to.name"
          :text="item.title"
          location="right"
          :disabled="!uiStore.drawerRail"
        >
          <template #activator="{ props }">
            <v-list-item
              v-bind="props"
              :to="item.to"
              rounded="lg"
              color="primary"
              class="mb-1 drawer-item"
              @click="smAndDown ? (uiStore.drawerRail = true) : null"
            >
              <template #prepend>
                <v-icon :icon="item.icon" size="20" class="drawer-icon" />
              </template>

              <template v-if="!uiStore.drawerRail" #title>
                <span class="text-caption font-weight-bold text-uppercase tracking-wider text-label-medium">
                  {{ item.title }}
                </span>
              </template>
            </v-list-item>
          </template>
        </v-tooltip>
      </v-list>
    </div>
  </v-navigation-drawer>
</template>

<script setup>
import { useDisplay } from 'vuetify'

import BrandLogo from '@/components/common/BrandLogo.vue'
import { APP_DRAWER_RAIL_WIDTH } from '@/config/layout'

import { useUiStore } from '@/stores/ui'

defineProps({
  items: {
    type: Array,
    required: true,
  },
})

const { smAndDown } = useDisplay()
const uiStore = useUiStore()
</script>

<style scoped>
.drawer-header {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 12px 12px 8px 12px;

  &.rail {
    justify-content: center;
    padding-inline: 0;
  }
}

.drawer-overlay {
  pointer-events: auto;
}

:deep(.v-list-item__prepend) {
  margin-inline-end: -12px !important;
}

:deep(.v-list-item) {
  min-height: 40px !important;
  padding-inline-start: 12px !important;
  padding-inline-end: 12px !important;
}

:deep(.v-navigation-drawer--rail .v-list-item) {
  padding-inline-start: 0 !important;
  padding-inline-end: 0 !important;
  display: flex !important;
  justify-content: center !important;
}

:deep(.v-navigation-drawer--rail .v-list-item__prepend) {
  margin-inline-end: 0 !important;
}

:deep(.v-list-item--active) {
  font-weight: 600;
}
</style>
