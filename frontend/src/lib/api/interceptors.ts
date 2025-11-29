import { AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios'

export const requestLogger = (config: InternalAxiosRequestConfig) => {
  const { method, url, params, data } = config
  console.log(`🚀 [${method?.toUpperCase()}] ${url}`, {
    params,
    data: data ? JSON.stringify(data).substring(0, 100) : undefined,
  })
  return config
}

export const responseLogger = (response: AxiosResponse) => {
  const { status, config } = response
  console.log(`✅ [${config.method?.toUpperCase()}] ${config.url} - ${status}`)
  return response
}

export const errorLogger = (error: AxiosError) => {
  if (error.response) {
    console.error(`❌ [${error.config?.method?.toUpperCase()}] ${error.config?.url}`, {
      status: error.response.status,
      data: error.response.data,
    })
  } else if (error.request) {
    console.error('❌ No response received:', error.message)
  } else {
    console.error('❌ Request error:', error.message)
  }
  return Promise.reject(error)
}
