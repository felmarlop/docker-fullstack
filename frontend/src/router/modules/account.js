import navigation from '@/navigation/account'

import AccountView from '@/views/account/AccountView.vue'

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
        //component: () => import('@/views/account/EmailView.vue'),
      },
      {
        path: 'password',
        name: 'account-password',
        //component: () => import('@/views/account/PasswordView.vue'),
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
