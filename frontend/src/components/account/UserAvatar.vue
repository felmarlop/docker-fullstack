<template>
  <div class="user-avatar-wrapper d-inline-block">
    <v-avatar :size="size" class="user-avatar">
      <v-img v-if="auth.user?.username" :src="auth.user?.avatar_url" :alt="auth.user.username">
        <template #placeholder>
          <div class="d-flex fill-height align-center justify-center bg-surface-light">
            <span class="text-high-emphasis" :style="{ fontSize: `${size / 3.5}px` }">
              {{ userLetters }}
            </span>
          </div>
        </template>
      </v-img>
    </v-avatar>

    <UserBadge v-if="showBadge" :badge-size="badgeSize" :badge-icon-size="badgeIconSize" />

    <!-- Edit Pill Button -->
    <v-menu v-if="showEdit" location="bottom start" offset="6">
      <template #activator="{ props: menuProps }">
        <v-btn
          v-bind="menuProps"
          variant="flat"
          color="surface"
          size="small"
          prepend-icon="mdi-pencil-outline"
          class="avatar-edit-pill border-color-soft px-3"
          :loading="loading"
          :disabled="loading"
        >
          Edit
        </v-btn>
      </template>

      <v-card min-width="180" variant="outlined" class="profile-menu-card bg-surface">
        <v-list density="comfortable" nav class="pa-1">
          <v-list-item rounded="lg" @click="openFilePicker">
            <div class="d-flex align-center">
              <v-icon icon="mdi-upload-outline" size="18" class="mr-2" />
              <span class="font-weight-medium">Upload a photo...</span>
            </div>
          </v-list-item>

          <v-list-item
            v-if="auth.user?.avatar_url"
            rounded="lg"
            color="error"
            class="text-error"
            @click="handleDeleteAvatar"
          >
            <div class="d-flex align-center">
              <v-icon icon="mdi-delete-outline" size="18" class="mr-2" />
              <span class="font-weight-medium">Remove photo</span>
            </div>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>

    <input
      ref="fileInput"
      type="file"
      accept="image/jpeg,image/png,image/webp"
      class="d-none"
      @change="handleFileChange"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import UserBadge from '@/components/account/UserBadge.vue'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const auth = useAuthStore()
const ui = useUiStore()

const props = defineProps({
  size: {
    type: Number,
    default: 40,
  },
  showEdit: {
    type: Boolean,
    default: false,
  },
  showBadge: {
    type: Boolean,
    default: true,
  },
})

const loading = ref(false)
const fileInput = ref(null)
const MAX_FILE_SIZE = 2 * 1024 * 1024 // 2MB Limit

const badgeSize = computed(() => Math.max(16, Math.round(props.size / 3.2)))
const badgeIconSize = computed(() => Math.max(10, Math.round(props.size / 5)))

const userLetters = computed(() => {
  let letters = ''
  if (auth.user?.first_name) {
    letters += auth.user?.first_name[0]
    if (auth.user?.last_name) {
      letters += auth.user?.last_name[0]
    } else {
      letters = ''
    }
  }
  if (auth.user?.username && !letters.length) {
    letters += auth.user?.username.slice(0, 2)
  }
  return letters.toUpperCase()
})

function openFilePicker() {
  fileInput.value?.click()
}

async function handleFileChange(event) {
  const file = event.target.files?.[0]
  if (!file) return

  if (file.size > MAX_FILE_SIZE) {
    ui.showError('Photo cannot exceed 2 MB.')
    event.target.value = ''
    return
  }

  try {
    await auth.changeAvatar(file)
    ui.showSuccess('Profile photo updated successfully.')
  } catch {
    ui.showError('Failed to upload photo. Please try again.')
  } finally {
    event.target.value = ''
  }
}

async function handleDeleteAvatar() {
  try {
    await auth.deleteAvatar()
    ui.showSuccess('Profile photo removed.')
  } catch {
    ui.showError('Failed to remove photo.')
  }
}
</script>

<style scoped>
.user-avatar-wrapper {
  position: relative;
}

.user-avatar {
  border: 2px solid rgba(var(--v-border-color), var(--v-border-opacity));
  background-color: rgb(var(--v-theme-surface)) !important;
}

:deep(.subscription-badge) {
  position: absolute;
  top: 0px;
  right: 0px;
  border: 1px solid rgb(var(--v-theme-surface)) !important;
  z-index: 2;
}

.avatar-edit-pill {
  position: absolute;
  right: 12px;
  bottom: 0px;
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
  text-transform: none !important;
  height: 28px !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08) !important;
}

.profile-menu-card {
  border-radius: 10px !important;
  border-color: rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

:deep(.v-list-item) {
  font-size: 0.875rem;
  min-height: 36px !important;
  padding-inline-start: 8px !important;
  padding-inline-end: 12px !important;
}
</style>
