<template>
  <v-container class="py-8" fluid>
    <div class="mx-auto account-content">
      <v-card rounded="lg" elevation="2" class="mb-10">
        <v-card-title class="d-flex align-center py-4 text-medium-emphasis">
          <span>My email address</span>
          <v-spacer />
          <v-btn
            variant="outlined"
            class="my-0 py-0"
            min-width="100"
            size="small"
            prepend-icon="mdi-pencil-outline"
            :class="{ invisible: emailState.editing }"
            @click="startEditingEmail"
          >
            EDIT
          </v-btn>
        </v-card-title>

        <v-divider />

        <template v-if="emailState.editing">
          <v-card-text>
            <v-alert v-if="emailState.error" class="mb-6" type="error" variant="tonal" density="comfortable">
              {{ emailState.error }}
            </v-alert>

            <v-form ref="emailFormRef" @submit.prevent="submitEmail">
              <v-text-field
                v-model="emailForm.email"
                label="New email"
                prepend-inner-icon="mdi-email-outline"
                autocomplete="email"
                variant="outlined"
                :rules="[rules.required, rules.email]"
                :error-messages="emailState.detailErrors.email"
                :disabled="emailState.loading"
              />

              <div class="d-flex justify-end ga-3 mt-2">
                <v-btn
                  variant="outlined"
                  min-width="120"
                  prepend-icon="mdi-close"
                  :disabled="emailState.loading"
                  @click="cancelEditingEmail"
                >
                  CANCEL
                </v-btn>

                <v-btn
                  type="submit"
                  color="primary"
                  min-width="120"
                  prepend-icon="mdi-content-save-outline"
                  :loading="emailState.loading"
                  :disabled="emailState.loading"
                >
                  UPDATE
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </template>

        <template v-else>
          <v-list lines="two">
            <v-list-item prepend-icon="mdi-email-outline" title="Email" :subtitle="userEmail || '-'">
              <template #append>
                <div v-if="auth.user?.pending_email" class="d-flex align-center text-warning">
                  <v-icon icon="mdi-progress-clock" size="18" />
                  <span class="ms-1">Verification pending</span>
                </div>
                <div v-else class="d-flex align-center text-success">
                  <v-icon icon="mdi-check-all" size="18" />
                  <span class="ms-1">Verified</span>
                </div>
              </template>
            </v-list-item>
            <template v-if="auth.user?.pending_email">
              <v-divider />
              <v-list-item class="pending-email">
                <div class="w-100">
                  <div class="text-medium-emphasis mb-3">
                    We've sent a verification email to your new email address. Please check your inbox.
                  </div>
                  <div class="d-flex justify-center">
                    <v-alert v-if="emailState.error" class="mb-6" type="error" variant="tonal" density="comfortable">
                      {{ emailState.error }}
                    </v-alert>

                    <v-form ref="emailFormRef" @submit.prevent="resendVerification">
                      <v-btn
                        type="submit"
                        color="primary"
                        variant="outlined"
                        prepend-icon="mdi-email-fast-outline"
                        :loading="emailState.loading"
                        :disabled="emailState.sent"
                      >
                        {{ emailState.sent ? 'EMAIL SENT' : 'RESEND VERIFICATION LINK' }}
                      </v-btn>
                    </v-form>
                  </div>
                </div>
              </v-list-item>
            </template>
          </v-list>
        </template>
      </v-card>

      <v-card rounded="lg" elevation="2">
        <v-card-title class="d-flex align-center py-4 text-medium-emphasis">
          <span>My password</span>

          <v-spacer />

          <v-btn
            variant="outlined"
            size="small"
            min-width="100"
            prepend-icon="mdi-pencil-outline"
            :class="{ invisible: passwordState.editing }"
            @click="startEditingPassword"
          >
            EDIT
          </v-btn>
        </v-card-title>

        <v-divider />

        <template v-if="passwordState.editing">
          <v-card-text>
            <v-alert v-if="passwordState.error" class="mb-6" type="error" variant="tonal" density="comfortable">
              {{ passwordState.error }}
            </v-alert>

            <v-form ref="passwordFormRef" @submit.prevent="submitPassword">
              <v-text-field
                v-model="passwordForm.current_password"
                label="Current password"
                :type="showCurrentPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="showCurrentPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                autocomplete="current-password"
                variant="outlined"
                :rules="[rules.required]"
                :error-messages="passwordState.detailErrors.current_password"
                :disabled="passwordState.loading"
                class="mb-4"
                @click:append-inner="showCurrentPassword = !showCurrentPassword"
              />

              <v-text-field
                v-model="passwordForm.new_password"
                label="New password"
                :type="showNewPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="showNewPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                autocomplete="new-password"
                variant="outlined"
                :rules="[rules.required]"
                :error-messages="passwordState.detailErrors.new_password"
                :disabled="passwordState.loading"
                @click:append-inner="showNewPassword = !showNewPassword"
              />

              <div class="d-flex justify-end ga-3 mt-2">
                <v-btn
                  variant="outlined"
                  min-width="120"
                  prepend-icon="mdi-close"
                  :disabled="passwordState.loading"
                  @click="cancelEditingPassword"
                >
                  CANCEL
                </v-btn>

                <v-btn
                  type="submit"
                  color="primary"
                  min-width="120"
                  prepend-icon="mdi-content-save-outline"
                  :loading="passwordState.loading"
                  :disabled="passwordState.loading"
                >
                  UPDATE
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </template>

        <template v-else>
          <v-list lines="two">
            <v-list-item title="Password" prepend-icon="mdi-lock-outline" subtitle="***************" />
          </v-list>
        </template>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'

import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

import * as authApi from '@/core/api/modules/auth'
import * as rules from '@/helpers/validation'

const auth = useAuthStore()
const ui = useUiStore()

const emailState = reactive({
  loading: false,
  editing: false,
  sent: false,
  error: '',
  detailErrors: {},
})
const passwordState = reactive({
  loading: false,
  editing: false,
  error: '',
  detailErrors: {},
})

const userEmail = computed(() => {
  return auth.user?.pending_email ?? auth.user?.email ?? ''
})

const emailFormRef = ref(null)
const passwordFormRef = ref(null)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)

const emailForm = reactive({
  email: '',
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
})

function startEditingEmail() {
  emailForm.email = userEmail.value

  emailState.error = ''
  emailState.detailErrors = {}
  emailState.editing = true
}

function cancelEditingEmail() {
  emailForm.email = ''

  emailState.error = ''
  emailState.detailErrors = {}
  emailState.editing = false
  emailState.loading = false
}

function startEditingPassword() {
  Object.assign(passwordForm, {
    current_password: '',
    new_password: '',
  })

  showCurrentPassword.value = false
  showNewPassword.value = false

  passwordState.error = ''
  passwordState.detailErrors = {}
  passwordState.editing = true
}

function cancelEditingPassword() {
  Object.assign(passwordForm, {
    current_password: '',
    new_password: '',
  })

  showCurrentPassword.value = false
  showNewPassword.value = false

  passwordState.error = ''
  passwordState.detailErrors = {}
  passwordState.editing = false
  passwordState.loading = false
}

async function submitEmail() {
  const { valid } = await emailFormRef.value.validate()
  if (!valid) return

  emailState.loading = true
  emailState.error = ''
  emailState.detailErrors = {}

  try {
    await auth.changeEmail(emailForm)

    cancelEditingEmail()
  } catch (err) {
    const details = err.details ?? null

    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      emailState.detailErrors = details
    } else {
      emailState.error = err.message ?? ''
    }
  } finally {
    emailState.loading = false
    emailState.sent = true
  }
}

async function submitPassword() {
  const { valid } = await passwordFormRef.value.validate()
  if (!valid) return

  passwordState.loading = true

  passwordState.error = ''
  passwordState.detailErrors = {}

  try {
    await authApi.changePassword(passwordForm)
    cancelEditingPassword()
  } catch (err) {
    const details = err.details ?? null

    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      passwordState.detailErrors = details
    } else {
      passwordState.error = err.message ?? ''
    }
  } finally {
    passwordState.loading = false
  }
}

async function resendVerification() {
  emailState.loading = true
  emailState.error = ''

  try {
    await authApi.resendVerificationEmail({ email: auth.user?.pending_email })

    emailState.sent = true
  } catch {
    ui.showError('Oops! An error occurred while sending the verification email.')
  } finally {
    emailState.loading = false
  }
}

watch(
  emailForm,
  () => {
    emailState.error = ''
  },
  {
    deep: true,
  },
)

watch(
  passwordForm,
  () => {
    passwordState.error = ''
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
      &.invisible {
        visibility: hidden;
      }
    }
  }

  .pending-email {
    font-size: 0.9rem !important;
  }
}
</style>
