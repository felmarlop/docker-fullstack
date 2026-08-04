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

    setAccessToken(accessToken) {
      this.accessToken = accessToken

      setCookie(ACCESS_TOKEN_COOKIE, accessToken)
    },

    setRefreshTokens(refreshToken) {
      this.refreshToken = refreshToken

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

      this.setAccessToken(accessToken)
      this.setRefreshTokens(refreshToken)

      try {
        const { data } = await usersApi.me()

        this.setUser(data)
      } catch {
        this.clearSession()
      }
    },

    async login(credentials) {
      const { data } = await authApi.login(credentials)

      this.setAccessToken(data.access)
      this.setRefreshTokens(data.refresh)
      this.setUser(data.user)

      return data
    },

    async register(payload) {
      const { data } = await authApi.register(payload)
      return data
    },

    async forgotPassword(payload) {
      const { data } = await authApi.forgotPassword(payload)
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
