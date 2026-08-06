import ActivateAccountView from '@/views/auth/ActivateAccountView.vue'
import ConfirmResetPasswordView from '@/views/auth/ConfirmResetPasswordView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import ResendActivationView from '@/views/auth/ResendActivationView.vue'
import ResetPasswordView from '@/views/auth/ResetPasswordView.vue'

export default [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      guestOnly: true,
    },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      guestOnly: true,
    },
  },
  {
    path: '/activate/:uidb64/:token',
    name: 'activate-account',
    component: ActivateAccountView,
    meta: {
      guestOnly: true,
    },
  },
  {
    path: '/resend',
    name: 'resend-activation',
    component: ResendActivationView,
    meta: {
      guestOnly: true,
    },
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: {
      guestOnly: true,
    },
  },
  {
    path: '/reset-password/:uidb64/:token',
    name: 'confirm-reset-password',
    component: ConfirmResetPasswordView,
    meta: {
      guestOnly: true,
    },
  },
]
