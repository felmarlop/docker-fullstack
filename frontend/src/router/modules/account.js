import navigation from '@/navigation/account'

import EmailPasswordView from '@/views/account/EmailPasswordView.vue'
import DeleteAccountView from '@/views/account/DeleteAccountView.vue'
import PersonalInfoView from '@/views/account/PersonalInfoView.vue'
import SubscriptionView from '@/views/account/SubscriptionView.vue'
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
        component: PersonalInfoView,
      },
      {
        path: 'security',
        name: 'account-security',
        component: EmailPasswordView,
      },
      {
        path: 'subscription',
        name: 'account-subscription',
        component: SubscriptionView,
      },
      {
        path: 'delete',
        name: 'account-delete',
        component: DeleteAccountView,
      },
    ],
  },
  {
    path: '/verify/email/:uidb64/:token',
    name: 'verify-email',
    component: VerifyEmailView,
  },
]
