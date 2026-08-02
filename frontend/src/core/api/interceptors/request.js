import { useAuthStore } from '@/stores/auth'

export default function setupRequestInterceptor(api) {
  api.interceptors.request.use(
    (config) => {
      const auth = useAuthStore()

      if (auth.accessToken) {
        config.headers = config.headers ?? {}
        config.headers.Authorization = `Bearer ${auth.accessToken}`
      }

      return config
    },
    (error) => Promise.reject(error),
  )
}
