/**
 * Media Resolver Utility
 * Seamlessly resolves Cloudinary HTTPS URLs, local backend /static/ assets, and fallbacks.
 */
export function resolveMediaUrl(path, fallback = null) {
  const backendBaseUrl = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:5000'

  if (!path || path === 'null' || path === 'undefined') {
    return fallback || `${backendBaseUrl}/static/Profile_pics/trekker.png`
  }

  // Already a full remote URL (Cloudinary, AWS, external CDN, data URI)
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }

  // Local static asset path from Flask backend
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${backendBaseUrl}${normalizedPath}`
}
