import api from '../index'

export function loginWithGoogle(data) {
  return api.post('oauth/google/', data)
}

export function loginWithGithub(data) {
  return api.post('oauth/github/', data)
}
