import api from '../index'

export function me() {
  return api.get('users/me/')
}

export function updateMe(data) {
  return api.put('users/me/', data)
}
