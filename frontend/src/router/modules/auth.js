import LoginView from '@/views/auth/LoginView.vue'
import ProfileView from '@/views/auth/ProfileView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'

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
    path: '/signup',
    name: 'signup',
    component: RegisterView,
    meta: {
      guestOnly: true,
    },
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: {
      requiresAuth: true,
    },
  },
]
