import { defineStore } from 'pinia'

import * as subscriptionApi from '@/core/api/modules/subscription'
import { useUiStore } from '@/stores/ui'

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    plans: [],
    loading: false,
    currentSubscription: null,
  }),

  actions: {
    setSubscription(subscription) {
      this.currentSubscription = subscription
    },
    async cancelSubscription(params) {
      if (!this.currentSubscription) return
      try {
        this.loading = true
        await subscriptionApi.cancel(this.currentSubscription.id, params)
        this.loading = false
        this.currentSubscription = null
        useUiStore().showSuccess('Your subscription has been cancelled. Your account is now on the Free Tier.')
      } catch {
        useUiStore().showError('An error occurred canceling your subscription. Please try again later')
      } finally {
        this.loading = false
      }
    },
    async getPlans() {
      try {
        const { data } = await subscriptionApi.getPlans()
        this.plans = data || {}
      } finally {
        this.loading = false
      }
    },
    async listSubscriptions() {
      try {
        this.loading = true
        const { data } = await subscriptionApi.list({ status__in: 'active,pending' })
        if (data.length) this.setSubscription(data[0])
      } catch {
        useUiStore().showError('An error occurred retrieving your subscriptions.')
      } finally {
        this.loading = false
      }
    },
    clear() {
      this.currentSubscription = null
    },
  },
})
