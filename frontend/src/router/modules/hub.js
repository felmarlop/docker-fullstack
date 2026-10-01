import navigation from '@/navigation/account'

import AgentIaView from '@/views/hub/AgentIaView.vue'

export default [
  {
    path: '/hub',
    name: 'hub',
    redirect: { name: 'hub-agent' },
    meta: {
      requiresAuth: true,
      navigation,
    },
    children: [
      {
        path: 'agent',
        name: 'hub-agent',
        component: AgentIaView,
      },
    ],
  },
]
