import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedUser: null,
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
      this.loggedUser = user
    },

    logout() {
      this.loggedUser = null
      this.accessToken = null
      this.refreshToken = null
    },
  },
})
