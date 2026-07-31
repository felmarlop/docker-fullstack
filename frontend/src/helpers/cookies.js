import { ACCESS_TOKEN_COOKIE, AUTH_COOKIE_DAYS, REFRESH_TOKEN_COOKIE } from '@/config/auth'

export function setCookie(name, value) {
  const expires = new Date()
  expires.setDate(expires.getDate() + AUTH_COOKIE_DAYS)
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`
}

export function getCookie(name) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`))
  return match ? decodeURIComponent(match[1]) : null
}

export function deleteCookie(name) {
  document.cookie = `${name}=; Max-Age=0; path=/`
}

export function getAuthCookies() {
  return {
    accessToken: getCookie(ACCESS_TOKEN_COOKIE),
    refreshToken: getCookie(REFRESH_TOKEN_COOKIE),
  }
}

export function clearAuthCookies() {
  deleteCookie(ACCESS_TOKEN_COOKIE)
  deleteCookie(REFRESH_TOKEN_COOKIE)
}
