import navigation from '@/navigation/account'

import AccountView from '@/views/account/AccountView.vue'
import EmailView from '@/views/account/EmailView.vue'
import PasswordView from '@/views/account/PasswordView.vue'

export default [
  {
    path: '/account',
    redirect: { name: 'account-profile' },
    meta: {
      requiresAuth: true,
      navigation,
    },
    children: [
      {
        path: 'profile',
        name: 'account-profile',
        component: AccountView,
      },
      {
        path: 'email',
        name: 'account-email',
        component: EmailView,
      },
      {
        path: 'password',
        name: 'account-password',
        component: PasswordView,
      },
      {
        path: 'subscription',
        name: 'account-subscription',
        //component: () => import('@/views/account/PasswordView.vue'),
      },
      {
        path: 'delete',
        name: 'account-delete',
        //component: () => import('@/views/account/DeleteAccountView.vue'),
      },
    ],
  },
]
