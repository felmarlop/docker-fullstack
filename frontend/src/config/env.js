export default {
  apiUrl: import.meta.env.VITE_API_URL,
  appName: import.meta.env.VITE_APP_NAME,
  githubClientId: import.meta.env.VITE_GITHUB_CLIENT_ID,
  googleClientId: import.meta.env.VITE_GOOGLE_CLIENT_ID,
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,

  snackbarTimeout: 6000,
}
