import { createVuetify } from 'vuetify'

const accushootTheme = {
  dark: false,
  colors: {
    primary: '#1976D2',
    secondary: '#424242',
    success: '#4CAF50',
    warning: '#FB8C00',
    error: '#D32F2F',
    info: '#2196F3',
    background: '#F5F5F5',
    surface: '#FFFFFF',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'accushootTheme',
    themes: {
      accushootTheme,
    },
  },
})
