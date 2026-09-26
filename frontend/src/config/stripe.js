import { loadStripe } from '@stripe/stripe-js'

export const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)

// Check plans here: backend/src/app/subscription/views/subscription.py
export const PLAN_PROPS = {
  'plus-lifetime': {
    icon: 'mdi-lightning-bolt-outline',
    color: 'plan1',
    class: 'plus-badge',
  },
  'pro-lifetime': {
    icon: 'mdi-star-outline',
    color: 'plan2',
    class: 'pro-badge',
  },
}
