<template>
  <v-container class="py-10" fluid>
    <div class="mx-auto account-content">
      <div class="text-center mb-8">
        <user-avatar :size="120" show-username />
        <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis mt-4">
          {{ auth.user?.username || '...' }}
        </h1>
      </div>

      <v-card variant="outlined" class="rounded-xl account-card">
        <v-card-item class="pa-6 border-b">
          <div class="d-flex align-center justify-space-between w-100">
            <div>
              <v-card-title class="text-h6 font-weight-bold"> Personal Information </v-card-title>
              <v-card-subtitle class="text-body-2 text-medium-emphasis">
                Manage your public profile details and account roles.
              </v-card-subtitle>
            </div>

            <v-btn
              variant="outlined"
              size="small"
              prepend-icon="mdi-pencil-outline"
              :class="{ invisible: editing }"
              class="font-weight-bold px-4"
              @click="startEditing"
            >
              Edit
            </v-btn>
          </div>
        </v-card-item>

        <template v-if="!editing">
          <v-list class="py-0">
            <v-list-item class="pa-6">
              <template #prepend>
                <v-avatar color="primary-lighten-5" size="40" class="mr-2">
                  <v-icon icon="mdi-account-outline" color="primary" size="20" />
                </v-avatar>
              </template>

              <!-- Label on top: Muted, small, structured -->
              <v-list-item-title class="text-caption font-weight-bold text-uppercase text-medium-emphasis mb-1">
                Full Name
              </v-list-item-title>

              <!-- Value on bottom: Large, crisp, prominent -->
              <v-list-item-subtitle
                class="text-body-1 text-high-emphasis font-weight-medium"
                :class="{ 'text-medium-emphasis': !fullName }"
                :style="{ 'font-style': fullName ? '' : 'italic' }"
              >
                {{ fullNameLabel }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider />

            <v-card-text class="pa-6 bg-grey-lighten-5">
              <p class="text-medium-emphasis mb-4">Permissions & Roles</p>

              <div class="d-flex justify-space-around align-center py-2">
                <div class="text-center">
                  <v-avatar
                    :color="auth.user?.is_staff ? 'primary-lighten-5' : 'grey-lighten-3'"
                    size="44"
                    class="mb-2"
                  >
                    <v-icon :color="auth.user?.is_staff ? 'primary' : 'medium-emphasis'" size="22">
                      mdi-shield-account-outline
                    </v-icon>
                  </v-avatar>
                  <div class="text-body-2 font-weight-bold text-high-emphasis">Administrator</div>
                  <div class="text-medium-emphasis">
                    {{ auth.user?.is_staff ? 'Yes' : 'No' }}
                  </div>
                </div>

                <v-divider vertical class="mx-4" />

                <div class="text-center">
                  <v-avatar
                    :color="auth.user?.is_superuser ? 'amber-lighten-5' : 'grey-lighten-3'"
                    size="44"
                    class="mb-2"
                  >
                    <v-icon :color="auth.user?.is_superuser ? 'amber-darken-2' : 'medium-emphasis'" size="22">
                      mdi-crown-outline
                    </v-icon>
                  </v-avatar>
                  <div class="text-body-2 font-weight-bold text-high-emphasis">Superuser</div>
                  <div class="text-medium-emphasis">
                    {{ auth.user?.is_superuser ? 'Yes' : 'No' }}
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-list>
        </template>

        <template v-else>
          <v-card-text class="pa-6">
            <v-alert
              v-if="error"
              type="error"
              variant="tonal"
              density="comfortable"
              icon="mdi-alert-circle-outline"
              class="mb-6 rounded-lg"
            >
              {{ error }}
            </v-alert>

            <v-form ref="formRef" @submit.prevent="submit">
              <div class="mb-4">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block"> Username </label>
                <v-text-field
                  v-model="form.username"
                  autofocus
                  placeholder="Username"
                  prepend-inner-icon="mdi-account-outline"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :error-messages="detailErrors.username"
                  :disabled="loading"
                />
              </div>

              <div class="mb-6">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block"> Full Name </label>
                <v-text-field
                  v-model="form.name"
                  placeholder="First and last name"
                  prepend-inner-icon="mdi-card-account-details-outline"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :error-messages="nameErrors"
                  :disabled="loading"
                />
              </div>

              <v-divider class="mb-6" />

              <div class="d-flex justify-end ga-3">
                <v-btn variant="text" color="default" :disabled="loading" @click="cancelEditing"> Cancel </v-btn>

                <v-btn
                  type="submit"
                  color="primary"
                  elevation="0"
                  size="large"
                  prepend-icon="mdi-content-save-outline"
                  :loading="loading"
                  :disabled="loading"
                  class="px-6 font-weight-bold"
                >
                  Save Changes
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </template>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'

import UserAvatar from '@/components/account/UserAvatar.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const loading = ref(false)
const editing = ref(false)
const formRef = ref(null)
const error = ref('')
const detailErrors = ref({})

const form = reactive({
  username: '',
  name: '',
})

const fullName = computed(() => {
  return [auth.user?.first_name, auth.user?.last_name].filter(Boolean).join(' ') || ''
})

const fullNameLabel = computed(() => {
  if (auth.user) {
    return [auth.user?.first_name, auth.user?.last_name].filter(Boolean).join(' ') || 'Not provided'
  }
  return '-'
})

const nameErrors = computed(() => {
  if ((detailErrors.value.first_name ?? []).length) {
    return detailErrors.value.first_name
  }
  return detailErrors.value.last_name
})

function startEditing() {
  Object.assign(form, {
    username: auth.user?.username ?? '',
    name: fullName.value,
  })
  error.value = ''
  detailErrors.value = {}
  editing.value = true
}

function cancelEditing() {
  error.value = ''
  detailErrors.value = {}
  editing.value = false
}

async function submit() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''
  detailErrors.value = {}

  try {
    const nameParts = form.name.trim().split(/\s+/)
    const payload = {
      username: form.username,
      first_name: nameParts.shift() ?? '',
      last_name: nameParts.join(' '),
    }

    await auth.updateMe(payload)
    editing.value = false
  } catch (err) {
    let details = err.details ?? null
    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      detailErrors.value = details
    } else {
      error.value = err.message ?? 'An unexpected error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

watch(
  form,
  () => {
    error.value = ''
  },
  {
    deep: true,
  },
)
</script>
