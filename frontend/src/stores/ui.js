import { defineStore } from 'pinia'

const STORAGE_KEY = 'drawer:rail'

function loadDrawerRail() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'false')
  } catch {
    return false
  }
}

export const useUiStore = defineStore('ui', {
  state: () => ({
    drawerRail: loadDrawerRail(),
    snackbar: {
      show: false,
      text: '',
      color: 'error',
    },
  }),

  actions: {
    toggleDrawerRail() {
      this.setDrawerRail(!this.drawerRail)
    },

    setDrawerRail(value) {
      this.drawerRail = value
      localStorage.setItem(STORAGE_KEY, JSON.stringify(value))
    },

    showSnackbar(text, color = 'error') {
      this.snackbar = {
        show: true,
        text,
        color,
      }
    },

    showError(text) {
      this.showSnackbar(text, 'error')
    },

    showSuccess(text) {
      this.showSnackbar(text, 'success')
    },

    hideSnackbar() {
      this.snackbar.show = false
    },
  },
})
