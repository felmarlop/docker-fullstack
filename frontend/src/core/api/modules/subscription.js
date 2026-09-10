import api from '../index'

export function getPlans() {
  return api.get(`subscription-plans/`)
}

export function get(subscriptionId) {
  return api.get(`subscriptions/${subscriptionId}/`)
}

export function list(params = {}) {
  return api.get(`subscriptions/`, { params })
}

export function create(data) {
  return api.post('subscriptions/create/', data)
}

export function cancel(subscriptionId, params = {}) {
  return api.post(`subscriptions/${subscriptionId}/cancel/`, params)
}
