<template>
  <v-container class="py-10" fluid>
    <div class="mx-auto account-content">
      <div class="mb-8">
        <h1 class="text-h4 font-weight-bold tracking-tight text-high-emphasis">Security & Credentials</h1>
      </div>

      <v-card variant="outlined" class="account-card mb-8">
        <v-card-item class="pa-6 border-b">
          <div class="d-flex align-center justify-space-between w-100">
            <div>
              <v-card-title class="text-h6 font-weight-bold"> Direct Email </v-card-title>
              <v-card-subtitle class="text-body-2 text-medium-emphasis">
                Primary email used for account authentication.
              </v-card-subtitle>
            </div>

            <v-btn
              variant="outlined"
              size="small"
              prepend-icon="mdi-pencil-outline"
              :class="{ invisible: emailState.editing }"
              class="font-weight-bold px-4"
              @click="startEditingEmail"
            >
              Edit
            </v-btn>
          </div>
        </v-card-item>

        <template v-if="!emailState.editing">
          <v-list class="py-0">
            <v-list-item class="pa-6">
              <template #prepend>
                <v-avatar color="primary-lighten-5" size="40" class="mr-2">
                  <v-icon icon="mdi-email-outline" color="primary" size="20" />
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-bold text-uppercase text-medium-emphasis mb-1">
                Email Address
              </v-list-item-title>

              <v-list-item-subtitle class="text-body-1 text-high-emphasis font-weight-medium">
                {{ userEmail || 'Not provided' }}
              </v-list-item-subtitle>

              <template #append>
                <v-chip
                  v-if="auth.user?.pending_email"
                  color="warning"
                  variant="tonal"
                  size="small"
                  prepend-icon="mdi-progress-clock"
                  class="font-weight-bold"
                >
                  Verification Pending
                </v-chip>

                <v-chip
                  v-else
                  color="success"
                  variant="tonal"
                  size="small"
                  prepend-icon="mdi-check-circle-outline"
                  class="font-weight-bold"
                >
                  Verified
                </v-chip>
              </template>
            </v-list-item>

            <template v-if="auth.user?.pending_email">
              <v-divider />
              <v-card-text class="pa-6 bg-grey-lighten-5">
                <div class="d-flex flex-column align-center text-center">
                  <p class="text-body-2 text-medium-emphasis mb-4">
                    We've sent a verification link to
                    <strong class="text-high-emphasis">{{ auth.user?.pending_email }}</strong
                    >. Please check your inbox.
                  </p>

                  <v-alert
                    v-if="emailState.error"
                    type="error"
                    variant="tonal"
                    density="comfortable"
                    icon="mdi-alert-circle-outline"
                    class="mb-4 rounded-lg w-100 text-left"
                  >
                    {{ emailState.error }}
                  </v-alert>

                  <v-form ref="emailFormRef" @submit.prevent="resendVerification">
                    <v-btn
                      type="submit"
                      variant="outlined"
                      color="primary"
                      prepend-icon="mdi-email-fast-outline"
                      :loading="emailState.loading"
                      :disabled="emailState.sent"
                      class="font-weight-bold"
                    >
                      {{ emailState.sent ? 'Verification Email Sent' : 'Resend Verification Link' }}
                    </v-btn>
                  </v-form>
                </div>
              </v-card-text>
            </template>
          </v-list>
        </template>

        <template v-else>
          <v-card-text class="pa-6">
            <v-alert
              v-if="emailState.error"
              type="error"
              variant="tonal"
              density="comfortable"
              icon="mdi-alert-circle-outline"
              class="mb-6 rounded-lg"
            >
              {{ emailState.error }}
            </v-alert>

            <v-form ref="emailFormRef" @submit.prevent="submitEmail">
              <div class="mb-6">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block">
                  New Email Address
                </label>
                <v-text-field
                  v-model="emailForm.email"
                  autofocus
                  placeholder="name@example.com"
                  prepend-inner-icon="mdi-email-outline"
                  autocomplete="email"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :rules="[rules.required, rules.email]"
                  :error-messages="emailState.detailErrors.email"
                  :disabled="emailState.loading"
                />
              </div>

              <v-divider class="mb-6" />

              <div class="d-flex justify-end ga-3">
                <v-btn variant="text" color="default" :disabled="emailState.loading" @click="cancelEditingEmail">
                  Cancel
                </v-btn>

                <v-btn
                  type="submit"
                  color="primary"
                  elevation="0"
                  size="large"
                  prepend-icon="mdi-content-save-outline"
                  :loading="emailState.loading"
                  :disabled="emailState.loading"
                  class="px-6 font-weight-bold"
                >
                  Update
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </template>
      </v-card>

      <v-card variant="outlined" class="account-card">
        <v-card-item class="pa-6 border-b">
          <div class="d-flex align-center justify-space-between w-100">
            <div>
              <v-card-title class="text-h6 font-weight-bold"> Password </v-card-title>
              <v-card-subtitle class="text-body-2 text-medium-emphasis">
                Set a secure password to protect your account.
              </v-card-subtitle>
            </div>

            <v-btn
              variant="outlined"
              size="small"
              prepend-icon="mdi-pencil-outline"
              :class="{ invisible: passwordState.editing }"
              class="font-weight-bold px-4"
              @click="startEditingPassword"
            >
              {{ usablePassword ? 'Edit' : 'Set password' }}
            </v-btn>
          </div>
        </v-card-item>

        <template v-if="!passwordState.editing">
          <v-list class="py-0">
            <v-list-item class="pa-6">
              <template #prepend>
                <v-avatar color="primary-lighten-5" size="40" class="mr-2">
                  <v-icon icon="mdi-lock-outline" color="primary" size="20" />
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-bold text-uppercase text-medium-emphasis mb-1">
                {{ usablePassword ? 'Current Password' : 'Password' }}
              </v-list-item-title>

              <v-list-item-subtitle
                class="text-body-1 text-high-emphasis font-weight-medium"
                :style="{ 'font-style': usablePassword ? '' : 'italic' }"
              >
                {{ passwordLabel }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </template>

        <template v-else>
          <v-card-text class="pa-6">
            <v-alert
              v-if="passwordState.error"
              type="error"
              variant="tonal"
              density="comfortable"
              icon="mdi-alert-circle-outline"
              class="mb-6 rounded-lg"
            >
              {{ passwordState.error }}
            </v-alert>

            <v-form ref="passwordFormRef" @submit.prevent="submitPassword">
              <div v-if="usablePassword" class="mb-4">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block">
                  Current Password
                </label>
                <v-text-field
                  v-model="passwordForm.current_password"
                  autofocus
                  placeholder="Enter current password"
                  :type="showCurrentPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock-outline"
                  :append-inner-icon="showCurrentPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  autocomplete="current-password"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :rules="[rules.required]"
                  :error-messages="passwordState.detailErrors.current_password"
                  :disabled="passwordState.loading"
                  @click:append-inner="showCurrentPassword = !showCurrentPassword"
                />
              </div>

              <div class="mb-6">
                <label class="font-weight-bold text-uppercase text-medium-emphasis mb-1 d-block"> New Password </label>
                <v-text-field
                  v-model="passwordForm.new_password"
                  :autofocus="!usablePassword"
                  placeholder="Enter new password"
                  :type="showNewPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock-reset"
                  :append-inner-icon="showNewPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  autocomplete="new-password"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                  :rules="[rules.required]"
                  :error-messages="passwordState.detailErrors.new_password"
                  :disabled="passwordState.loading"
                  @click:append-inner="showNewPassword = !showNewPassword"
                />
              </div>

              <v-divider class="mb-6" />

              <div class="d-flex justify-end ga-3">
                <v-btn variant="text" color="default" :disabled="passwordState.loading" @click="cancelEditingPassword">
                  Cancel
                </v-btn>

                <v-btn
                  type="submit"
                  color="primary"
                  elevation="0"
                  size="large"
                  prepend-icon="mdi-content-save-outline"
                  :loading="passwordState.loading"
                  :disabled="passwordState.loading"
                  class="px-6 font-weight-bold"
                >
                  Update
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

const usablePassword = computed(() => {
  return auth.user?.has_usable_password ?? false
})

const passwordLabel = computed(() => {
  return usablePassword.value ? '••••••••••••••••' : 'No password has been set for this account.'
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
      emailState.error = err.message ?? 'An error occurred while updating your email.'
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
    await auth.changePassword(passwordForm)
    cancelEditingPassword()
  } catch (err) {
    const details = err.details ?? null

    if (details && typeof details === 'object' && Object.keys(details).length > 0) {
      passwordState.detailErrors = details
    } else {
      passwordState.error = err.message ?? 'An error occurred while changing your password.'
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
  { deep: true },
)

watch(
  passwordForm,
  () => {
    passwordState.error = ''
  },
  { deep: true },
)
</script>
