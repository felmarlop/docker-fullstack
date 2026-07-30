import { defineStore } from 'pinia'

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
    setTokens(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
    },

    setUser(user) {
      this.user = user
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
    },
  },
})
