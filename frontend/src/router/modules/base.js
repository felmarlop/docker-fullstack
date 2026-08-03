import HomeView from '@/views/base/HomeView.vue'
import NotFoundView from '@/views/base/NotFoundView.vue'

export default [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      guestOnly: true,
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
  },
]
