import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import baseRoutes from './modules/base'
import authRoutes from './modules/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [...baseRoutes, ...authRoutes],

  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login' }
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'profile' }
  }
})

export default router
