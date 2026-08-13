<template>
  <v-navigation-drawer
    v-model:rail="uiStore.drawerRail"
    :rail-width="APP_DRAWER_RAIL_WIDTH"
    permanent
  >
    <div
      class="drawer-header"
      :class="{ rail: uiStore.drawerRail }"
    >
      <v-btn
        :icon="uiStore.drawerRail ? 'mdi-chevron-right' : 'mdi-chevron-left'"
        variant="text"
        density="comfortable"
        @click="uiStore.toggleDrawerRail()"
      />
    </div>

    <v-list
      density="comfortable"
      class="py-2"
    >
      <v-tooltip
        v-for="item in items"
        :key="item.to.name"
        :text="item.title"
        :nav="!uiStore.drawerRail"
        location="right"
        :disabled="!uiStore.drawerRail"
      >
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            :to="item.to"
            :title="uiStore.drawerRail ? undefined : item.title"
            class="mx-2 mb-1"
            rounded="lg"
          >
            <template #prepend>
              <v-icon :icon="item.icon" />
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
  justify-content: flex-end;
  padding: 12px 8px;
}

.drawer-header.rail {
  justify-content: center;
}

:deep(.v-list-item-title) {
  font-size: 0.95rem;
  font-weight: 500;
  color: rgb(var(--v-theme-on-surface));
}

:deep(.v-list-item) {
  padding-right: 0;
  transition: all 0.2s ease;
}

:deep(.v-list-item__prepend > .v-icon) {
  font-size: 20px;
}

:deep(.v-navigation-drawer--rail .v-list-item__prepend > .v-icon) {
  margin-inline: 0;
}

:deep(.v-navigation-drawer--rail .v-list-item) {
  padding-inline: 0;
}
</style>
