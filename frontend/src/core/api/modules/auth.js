import api from '../index'

export function login(data) {
  return api.post('auth/login/', data)
}

export function register(data) {
  return api.post('auth/register/', data)
}

export function activate(uidb64, token) {
  return api.get(`auth/activate/${uidb64}/${token}/`)
}

export function refresh(refreshToken) {
  return api.post('auth/refresh/', {
    refresh: refreshToken,
  })
}

export function resendActivationEmail(data) {
  return api.post(`auth/activate/resend/`, data)
}

export function changeEmail(data) {
  return api.post('auth/change-email/', data)
}

export function verifyEmail(uidb64, token) {
  return api.get(`auth/verify-email/${uidb64}/${token}/`)
}

export function resendVerificationEmail(data) {
  return api.post(`auth/verify-email/resend/`, data)
}

export function changePassword(data) {
  return api.post('auth/change-password/', data)
}

export function forgotPassword(data) {
  return api.post('auth/forgot-password/', data)
}

export function resetPassword(data) {
  return api.post(`auth/reset-password/`, data)
}

export function logout(refreshToken) {
  return api.post('auth/logout/', {
    refresh: refreshToken,
  })
}

export function deleteAccount(data) {
  return api.post('auth/delete-account/', data)
}
