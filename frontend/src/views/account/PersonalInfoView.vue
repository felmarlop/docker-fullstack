<template>
  <v-container class="py-8" fluid>
    <div class="mx-auto account-content">
      <div class="text-center">
        <user-avatar :size="180" show-username />
        <h1 class="text-h1 font-weight-bold mt-4 text-center">
          {{ auth.user?.username }}
        </h1>
      </div>

      <v-card rounded="lg" elevation="2">
        <v-card-title class="d-flex align-center py-4 text-medium-emphasis">
          <span>Personal information</span>
          <v-spacer />
          <v-btn
            variant="outlined"
            min-width="100"
            size="small"
            prepend-icon="mdi-pencil-outline"
            :class="{ invisible: editing }"
            @click="startEditing"
          >
            EDIT
          </v-btn>
        </v-card-title>

        <v-divider />

        <template v-if="!editing">
          <v-list lines="two">
            <v-list-item
              prepend-icon="mdi-account-outline"
              title="Name"
              :style="{ 'font-style': fullName ? '' : 'italic' }"
              :subtitle="fullName || 'Not provided'"
            />

            <v-divider />

            <v-list-item>
              <div class="d-flex justify-space-around align-center py-2">
                <div class="text-center">
                  <v-icon :color="auth.user?.is_staff ? 'primary' : 'medium-emphasis'" size="28">
                    mdi-shield-account-outline
                  </v-icon>

                  <div class="text-body-2 mt-1">Administrator</div>

                  <div class="text-medium-emphasis">
                    {{ auth.user?.is_staff ? 'Yes' : 'No' }}
                  </div>
                </div>

                <div class="text-center">
                  <v-icon :color="auth.user?.is_superuser ? 'secondary' : 'medium-emphasis'" size="28">
                    mdi-crown-outline
                  </v-icon>

                  <div class="text-body-2 mt-1">Superuser</div>

                  <div class="text-medium-emphasis">
                    {{ auth.user?.is_superuser ? 'Yes' : 'No' }}
                  </div>
                </div>
              </div>
            </v-list-item>
          </v-list>
        </template>

        <template v-else>
          <v-card-text>
            <v-alert v-if="error" class="mb-6" type="error" variant="tonal" density="comfortable">
              {{ error }}
            </v-alert>

            <v-form ref="formRef" @submit.prevent="submit">
              <v-text-field
                v-model="form.username"
                label="Username"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
                :error-messages="detailErrors.username"
                :disabled="loading"
                class="mb-4"
              />

              <v-text-field
                v-model="form.name"
                label="Name"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
                :error-messages="nameErrors"
                :disabled="loading"
              />

              <div class="d-flex justify-end ga-3 mt-2">
                <v-btn
                  variant="outlined"
                  min-width="120"
                  prepend-icon="mdi-close"
                  :disabled="loading"
                  @click="cancelEditing"
                >
                  CANCEL
                </v-btn>

                <v-btn
                  type="submit"
                  color="primary"
                  min-width="120"
                  prepend-icon="mdi-content-save-outline"
                  :loading="loading"
                  :disabled="loading"
                >
                  UPDATE
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
      error.value = err.message ?? ''
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
