import axios from 'axios'

import env from '@/config/env'

import setupRequestInterceptor from './interceptors/request'
import setupResponseInterceptor from './interceptors/response'

const api = axios.create({
  baseURL: env.apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
})

setupRequestInterceptor(api)
setupResponseInterceptor(api)

export default api
