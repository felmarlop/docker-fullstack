import api from '../index'

export function loginWithGoogle(data) {
  return api.post('auth/social/google/', data)
}
