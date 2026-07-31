import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({
    snackbar: {
      show: false,
      text: '',
      color: 'error',
    },
  }),

  actions: {
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
