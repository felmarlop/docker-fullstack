import navigation from '@/navigation/account'

import AccountView from '@/views/account/AccountView.vue'
import EmailPasswordView from '@/views/account/EmailPasswordView.vue'
import VerifyEmailView from '@/views/account/VerifyEmailView.vue'

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
        path: 'security',
        name: 'account-security',
        component: EmailPasswordView,
      },
      {
        path: 'subscription',
        name: 'account-subscription',
        //component: EmailPasswordView,
      },
      {
        path: 'delete',
        name: 'account-delete',
        //component: () => import('@/views/account/DeleteAccountView.vue'),
      },
    ],
  },
  {
    path: '/verify/email/:uidb64/:token',
    name: 'verify-email',
    component: VerifyEmailView,
  },
]
