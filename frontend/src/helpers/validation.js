export const required = (value) => !!value || 'Field required'

export const email = (value) => !value || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || 'Enter a valid email'

export const minLength = (length) => (value) =>
  !value || value.length >= length || `Must contain at least ${length} characters`
