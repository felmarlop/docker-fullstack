import { loadStripe } from '@stripe/stripe-js'

export const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)

// Check plans here: backend/src/app/subscription/views/subscription.py
export const PLAN_PROPS = {
  'pro-lifetime': {
    icon: 'mdi-star-outline',
    color: 'accent',
    class: 'pro-badge',
  },
  'plus-lifetime': {
    icon: 'mdi-lightning-bolt-outline',
    color: 'primary',
    class: 'plus-badge',
  },
}
