import { useUiStore } from '@/stores/ui'

const GENERAL_ERROR_MESSAGE = 'Unable to connect to the server.'

export function handleApiError(error, notify = false) {
  let apiError
  if (!error.response) {
    apiError = {
      status: 0,
      code: 'network_error',
      message: GENERAL_ERROR_MESSAGE,
      details: null,
    }
  } else {
    const { status, data } = error.response

    apiError = {
      status,
      code: data.code || 'unknown_error',
      message: data.message || GENERAL_ERROR_MESSAGE,
      details: data.errors || null,
    }
  }
  if (notify) showGlobalError(apiError)
  return apiError
}

function showGlobalError(error) {
  const ui = useUiStore()
  let message
  switch (error.status) {
    case 401:
      message = error.message || 'Authentication required.'
      break

    case 403:
      message = error.message || 'You do not have permission.'
      break

    case 404:
      message = error.message || 'Resource not found.'
      break

    case 422:
      message = error.message || 'Invalid request data.'
      break

    case 500:
      message = error.message || 'Internal server error.'
      break

    default:
      message = error.message || GENERAL_ERROR_MESSAGE
      break
  }

  ui.showError(message)
}
