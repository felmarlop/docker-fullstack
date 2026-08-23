<template>
  <v-navigation-drawer
    v-model:rail="uiStore.drawerRail"
    :rail-width="APP_DRAWER_RAIL_WIDTH"
    permanent
    class="app-drawer border-e"
  >
    <div class="drawer-header" :class="{ rail: uiStore.drawerRail }">
      <v-btn
        :icon="uiStore.drawerRail ? 'mdi-chevron-right' : 'mdi-chevron-left'"
        variant="text"
        density="comfortable"
        color="primary"
        @click="uiStore.toggleDrawerRail()"
      />
    </div>

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
            :title="uiStore.drawerRail ? undefined : item.title"
            rounded="lg"
            color="primary"
            class="mb-1 drawer-item"
          >
            <template #prepend>
              <v-icon :icon="item.icon" size="20" class="drawer-icon" />
            </template>
          </v-list-item>
        </template>
      </v-tooltip>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { APP_DRAWER_RAIL_WIDTH } from '@/config/layout'
import { useUiStore } from '@/stores/ui'

defineProps({
  items: {
    type: Array,
    required: true,
  },
})

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

:deep(.v-list-item-title) {
  font-weight: 500 !important;
  letter-spacing: -0.01em !important;
}

:deep(.v-list-item__prepend) {
  margin-inline-end: 12px !important;
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
