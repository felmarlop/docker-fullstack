import api from '../index'

export function login(payload) {
  return api.post('auth/login/', payload)
}

export function register(payload) {
  return api.post('auth/register/', payload)
}

export function activate(uidb64, token) {
  return api.get(`auth/activate/${uidb64}/${token}/`)
}

export function resendActivationEmail(payload) {
  return api.post(`auth/activate/resend/`, payload)
}

export function forgotPassword(payload) {
  return api.post('auth/forgot-password/', payload)
}

export function resetPassword(payload) {
  return api.post(`auth/reset-password/`, payload)
}

export function logout(refreshToken) {
  return api.post('auth/logout/', {
    refresh: refreshToken,
  })
}

export function refresh(refreshToken) {
  return api.post('auth/refresh/', {
    refresh: refreshToken,
  })
}
