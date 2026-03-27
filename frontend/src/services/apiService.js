import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const apiService = {
  // Authentication
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),

  // Products
  getProducts: () => api.get('/products'),
  getProduct: (id) => api.get(`/products/${id}`),
  createProduct: (data) => api.post('/products', data),
  updateProduct: (id, data) => api.put(`/products/${id}`, data),
  deleteProduct: (id) => api.delete(`/products/${id}`),
  getProductsByCategory: (category) => api.get(`/products/by-category/${category}`),

  // Orders
  getOrders: () => api.get('/orders'),
  createOrder: (data) => api.post('/orders', data),
  updateOrderStatus: (id, data) => api.put(`/orders/${id}`, data),

  // Users
  getUsers: () => api.get('/users'),
  getUser: (id) => api.get(`/users/${id}`),
  updateUser: (id, data) => api.put(`/users/${id}`, data),
  deleteUser: (id) => api.delete(`/users/${id}`),

  // Wishlist
  addToWishlist: (userId, productId) => 
    api.post(`/users/${userId}/wishlist`, { product_id: productId }),
  removeFromWishlist: (userId, productId) => 
    api.delete(`/users/${userId}/wishlist/${productId}`),

  // Analytics
  getDashboardAnalytics: () => api.get('/analytics/dashboard'),

  // Categories
  getCategories: () => api.get('/categories'),
  createCategory: (data) => api.post('/categories', data),
  updateCategory: (id, data) => api.put(`/categories/${id}`, data),
  deleteCategory: (id) => api.delete(`/categories/${id}`),

  // Uploads
  uploadImage: (formData) => api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }),

  // Change Password
  changePassword: (data) => api.post('/auth/change-password', data),

  // Cancel Order
  cancelOrder: (orderId) => api.put(`/orders/${orderId}/cancel`),

  // Coupons
  validateCoupon: (data) => api.post('/coupons/validate', data),
  getCoupons: () => api.get('/coupons'),

  // Reviews
  submitReview: (data) => api.post(`/products/${data.product_id}/reviews`, data),

  // Export
  exportReport: () => api.get('/analytics/export', { responseType: 'blob' }),
}

export default api
