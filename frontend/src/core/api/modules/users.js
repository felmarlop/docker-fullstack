import api from '../index'

export function me() {
  return api.get('users/me/')
}
