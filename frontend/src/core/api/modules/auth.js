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

export function forgotPassword(payload) {
  return api.post('auth/forgot-password/', payload)
}

export function resetPassword(uidb64, token, newPassword) {
  return api.post(`auth/reset-password/`, {
    uidb64,
    token,
    new_password: newPassword,
  })
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
