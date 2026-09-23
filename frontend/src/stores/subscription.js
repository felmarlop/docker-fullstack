import { defineStore } from 'pinia'

import * as subscriptionApi from '@/core/api/modules/subscription'
import { useUiStore } from '@/stores/ui'

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    plans: [],
    loading: false,
    loadingSubscription: null,
    subscriptions: [],
  }),

  getters: {
    pendingSubscription(state) {
      return state.subscriptions.find((s) => s.status === 'pending') || null
    },
    currentSubscription(state) {
      return state.subscriptions.find((s) => s.status === 'active') || this.pendingSubscription || null
    },
  },

  actions: {
    setSubscriptions(subscriptions) {
      this.subscriptions = subscriptions
    },
    async resumePayment() {
      if (!this.pendingSubscription) {
        useUiStore().showError('We could not find a pending subscription. Please try again later')
        return
      }
      try {
        this.loadingSubscription = this.pendingSubscription.id
        const { data } = await subscriptionApi.resume(this.pendingSubscription.id)
        return data
      } catch {
        useUiStore().showError('An error occurred with your payment. Please try again later')
      } finally {
        this.loadingSubscription = null
      }
    },
    async syncPendingPayment() {
      if (!this.pendingSubscription) {
        useUiStore().showError('We could not find a pending subscription. Please try again later')
        return
      }
      try {
        this.loadingSubscription = this.pendingSubscription.id
        await subscriptionApi.sync(this.pendingSubscription.id)
      } catch {
        useUiStore().showError('An error occurred with your payment. Please try again later')
      } finally {
        await this.listSubscriptions()
        this.loadingSubscription = null
      }
    },
    async cancelCurrentSubscription(params) {
      if (!this.currentSubscription) {
        useUiStore().showError('We could not find your subscription. Please try again later')
        return
      }
      try {
        this.loadingSubscription = this.currentSubscription.id
        await subscriptionApi.cancel(this.currentSubscription.id, params)
        useUiStore().showSuccess('Your subscription has been cancelled correctly.')
      } catch {
        useUiStore().showError('An error occurred canceling your subscription. Please try again later')
      } finally {
        this.loadingSubscription = null
      }
    },
    async cancelPendingSubscription(params) {
      if (!this.pendingSubscription) {
        useUiStore().showError('We could not find the pending subscription. Please try again later')
        return
      }
      try {
        this.loadingSubscription = this.pendingSubscription.id
        await subscriptionApi.cancel(this.pendingSubscription.id, params)
      } catch {
        useUiStore().showError('An error occurred canceling the pending subscription. Please try again later')
      } finally {
        this.loadingSubscription = null
      }
    },
    async getPlans() {
      try {
        this.loading = true
        const { data } = await subscriptionApi.getPlans()
        this.plans = data || []
      } catch {
        useUiStore().showError('An error occurred retrieving the subscription plans.')
      } finally {
        this.loading = false
      }
    },
    async listSubscriptions() {
      try {
        this.loading = true
        const { data } = await subscriptionApi.list({ status__in: 'active,pending' })
        this.setSubscriptions(data?.results || [])
      } catch {
        useUiStore().showError('An error occurred retrieving your subscriptions.')
      } finally {
        this.loading = false
      }
    },
    clear() {
      this.subscriptions = []
    },
  },
})
