import { defineStore } from 'pinia'

import * as authApi from '@/core/api/modules/auth'
import * as usersApi from '@/core/api/modules/users'

import { ACCESS_TOKEN_COOKIE, REFRESH_TOKEN_COOKIE } from '@/config/auth'

import { clearAuthCookies, getAuthCookies, setCookie } from '@/helpers/cookies'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
  }),

  getters: {
    isAuthenticated: (state) => state.accessToken !== null,
  },

  actions: {
    setUser(user) {
      this.user = user
    },

    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken
      this.refreshToken = refreshToken

      setCookie(ACCESS_TOKEN_COOKIE, accessToken)
      setCookie(REFRESH_TOKEN_COOKIE, refreshToken)
    },

    clearSession() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null

      clearAuthCookies()
    },

    async initialize() {
      const { accessToken, refreshToken } = getAuthCookies()
      if (!accessToken || !refreshToken) return

      this.setTokens(accessToken, refreshToken)

      try {
        const { data } = await usersApi.me()

        this.setUser(data)
      } catch {
        this.clearSession()
      }
    },

    async login(credentials) {
      const { data } = await authApi.login(credentials)

      this.setTokens(data.access, data.refresh)
      this.setUser(data.user)

      return data
    },

    async logout() {
      try {
        await authApi.logout(this.refreshToken)
      } catch {
        // Ignore backend errors.
      } finally {
        this.clearSession()
      }
    },
  },
})
