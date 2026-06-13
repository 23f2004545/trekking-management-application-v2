import { useAuthStore } from '../stores/auth'

export async function secureFetch(url, options = {}) {
  const authStore = useAuthStore()

  // 1. Inject the active token into headers
  options.headers = {
    ...options.headers,
    'Authorization': `Bearer ${authStore.token}`
  }

  // 2. Make the initial request
  let response = await fetch(url, options)

  // 3. Catch expiration instantly
  if (response.status === 401) {
    console.warn("Access token expired. Attempting refresh lifecycle...")
    
    // Attempt to refresh the token via Pinia
    const refreshSuccessful = await authStore.attemptTokenRefresh()
    
    if (refreshSuccessful) {
      // If successful, update the header with the NEW token and retry!
      options.headers['Authorization'] = `Bearer ${authStore.token}`
      response = await fetch(url, options)
    } else {
      console.error("Refresh token invalid or expired. Session terminated.")
      // The Pinia store handles the logout automatically based on your code
    }
  }

  return response
}