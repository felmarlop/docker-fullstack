export default function setupRequestInterceptor(api) {
  api.interceptors.request.use(
    (config) => config,
    (error) => Promise.reject(error),
  )
}
