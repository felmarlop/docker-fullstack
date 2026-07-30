import axios from 'axios'

import env from '@/config/env'

import requestInterceptor from './interceptors/request'
import responseInterceptor from './interceptors/response'

const api = axios.create({
  baseURL: env.apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(requestInterceptor)

api.interceptors.response.use((response) => response, responseInterceptor)

export default api
