import { handleApiError } from '../error-handler'

export default function setupResponseInterceptor(api) {
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      const { notify = false } = error.config ?? {}
      return Promise.reject(handleApiError(error, notify))
    },
  )
}
