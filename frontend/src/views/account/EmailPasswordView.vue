<template>
  <v-container class="py-8" fluid>
    <div class="mx-auto account-content">
			<v-card rounded="lg" elevation="2" class="mb-10">
        <v-card-title class="d-flex align-center py-4 text-medium-emphasis">
          <span>My email address</span>
          <v-spacer />
          <v-btn
            v-if="!editing"
            variant="outlined"
            min-width="100"
            size="small"
            prepend-icon="mdi-pencil-outline"
          >
            EDIT
          </v-btn>
        </v-card-title>

        <v-divider />

        <template v-if="!editing">
          <v-list lines="two">
            <v-list-item
              prepend-icon="mdi-email-outline"
              title="Email"
              :subtitle="auth.user?.email || '-'"
            />
          </v-list>
        </template>

        <template v-else>
          <v-card-text>
            <v-form ref="formRef">
            </v-form>
          </v-card-text>
        </template>
      </v-card>

      <v-card rounded="lg" elevation="2">
        <v-card-title class="d-flex align-center py-4 text-medium-emphasis">
          <span>My password</span>

          <v-spacer />

          <v-btn
            v-if="!editing"
            variant="outlined"
            size="small"
            min-width="100"
            prepend-icon="mdi-pencil-outline"
            @click="startEditing"
          >
            EDIT
          </v-btn>
        </v-card-title>

        <v-divider />

        <template v-if="!editing">
          <v-list lines="two">
						<v-list-item
							title="Password"
							prepend-icon="mdi-key-variant"
							subtitle="***************"
						/>
					</v-list>
        </template>

        <template v-else>
          <v-card-text>
            <v-alert
              v-if="error"
              class="mb-6"
              type="error"
              variant="tonal"
              density="comfortable"
            >
              {{ error }}
            </v-alert>

            <v-form ref="formRef" @submit.prevent="submit">
              <v-text-field
                v-model="form.current_password"
                label="Current password"
                :type="showCurrentPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="
                  showCurrentPassword
                    ? 'mdi-eye-off-outline'
                    : 'mdi-eye-outline'
                "
                autocomplete="current-password"
                variant="outlined"
								:rules="[rules.required]"
                :error-messages="detailErrors.current_password"
                :disabled="loading"
                class="mb-4"
                @click:append-inner="
                  showCurrentPassword = !showCurrentPassword
                "
              />

              <v-text-field
                v-model="form.new_password"
                label="New password"
                :type="showNewPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="
                  showNewPassword
                    ? 'mdi-eye-off-outline'
                    : 'mdi-eye-outline'
                "
                autocomplete="new-password"
                variant="outlined"
								:rules="[rules.required]"
                :error-messages="detailErrors.new_password"
                :disabled="loading"
                @click:append-inner="
                  showNewPassword = !showNewPassword
                "
              />

              <div class="d-flex justify-end ga-3 mt-6">
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
import { reactive, ref, watch } from 'vue'

import { useAuthStore } from '@/stores/auth'

import * as authApi from '@/core/api/modules/auth'
import * as rules from '@/helpers/validation'

const auth = useAuthStore()

const loading = ref(false)
const editing = ref(false)
const formRef = ref(null)
const error = ref('')
const detailErrors = ref({})
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)

const form = reactive({
  current_password: '',
  new_password: '',
})

function startEditing() {
  Object.assign(form, {
    current_password: '',
    new_password: '',
  })

  showCurrentPassword.value = false
  showNewPassword.value = false

  error.value = ''
  detailErrors.value = {}

  editing.value = true
}

function cancelEditing() {
  Object.assign(form, {
    current_password: '',
    new_password: '',
  })

  showCurrentPassword.value = false
  showNewPassword.value = false

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
    await authApi.changePassword(form)
    cancelEditing()
  } catch (err) {
    const details = err.details ?? null

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

<style scoped>
.account-content {
  max-width: 760px;

  .v-card-title {
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    .v-btn {
      font-size: 0.8rem !important;
    }
  }
}
</style>
