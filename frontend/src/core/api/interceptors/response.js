import router from '@/router'
import { useAuthStore } from '@/stores/auth'
import * as authApi from '@/core/api/modules/auth'

import { handleApiError } from '../error-handler'

export default function setupResponseInterceptor(api) {
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const auth = useAuthStore()

      const { config, response } = error
      const { notify = false } = config ?? {}

      if (
        response?.status === 401 &&
        auth.refreshToken &&
        config &&
        !config._retry &&
        !config.url?.includes('/refresh/')
      ) {
        try {
          config._retry = true

          const { data } = await authApi.refresh(auth.refreshToken)
          auth.setAccessToken(data.access)

          config.headers = config.headers ?? {}
          config.headers.Authorization = `Bearer ${data.access}`

          return api.request(config)
        } catch {
          auth.clearSession()
          await router.push({ name: 'login' })
        }
      }

      return Promise.reject(handleApiError(error, notify))
    },
  )
}
