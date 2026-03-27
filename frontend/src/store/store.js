import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('user')) || null,
  token: localStorage.getItem('token') || null,
  isAuthenticated: !!localStorage.getItem('token') && localStorage.getItem('token') !== 'null',

  login: (user, token) => {
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('token', token)
    set({
      user,
      token,
      isAuthenticated: true,
    })
  },

  logout: () => {
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
  },

  updateUser: (user) => {
    localStorage.setItem('user', JSON.stringify(user))
    set({ user })
  },
}))

export const useCartStore = create((set, get) => ({
  items: JSON.parse(localStorage.getItem('cart')) || [],

  addItem: (product, quantity, selectedColor = null, selectedSize = null) => {
    const { items } = get()
    // Use a unique key that combines product_id, color, and size
    const existingItem = items.find((item) => 
      item.product_id === product.product_id && 
      item.selectedColor === selectedColor && 
      item.selectedSize === selectedSize
    )

    if (existingItem) {
      const updatedItems = items.map((item) =>
        (item.product_id === product.product_id && 
         item.selectedColor === selectedColor && 
         item.selectedSize === selectedSize)
          ? { ...item, quantity: item.quantity + quantity }
          : item
      )
      localStorage.setItem('cart', JSON.stringify(updatedItems))
      set({ items: updatedItems })
    } else {
      const newItems = [...items, { ...product, quantity, selectedColor, selectedSize }]
      localStorage.setItem('cart', JSON.stringify(newItems))
      set({ items: newItems })
    }
  },

  removeItem: (productId, selectedColor = null, selectedSize = null) => {
    const { items } = get()
    const updatedItems = items.filter((item) => 
      !(item.product_id === productId && 
        item.selectedColor === selectedColor && 
        item.selectedSize === selectedSize)
    )
    localStorage.setItem('cart', JSON.stringify(updatedItems))
    set({ items: updatedItems })
  },

  updateQuantity: (productId, quantity, selectedColor = null, selectedSize = null) => {
    const { items } = get()
    if (quantity <= 0) {
      const updatedItems = items.filter((item) => 
        !(item.product_id === productId && 
          item.selectedColor === selectedColor && 
          item.selectedSize === selectedSize)
      )
      localStorage.setItem('cart', JSON.stringify(updatedItems))
      set({ items: updatedItems })
    } else {
      const updatedItems = items.map((item) =>
        (item.product_id === productId && 
         item.selectedColor === selectedColor && 
         item.selectedSize === selectedSize) 
          ? { ...item, quantity } 
          : item
      )
      localStorage.setItem('cart', JSON.stringify(updatedItems))
      set({ items: updatedItems })
    }
  },

  clearCart: () => {
    localStorage.removeItem('cart')
    set({ items: [] })
  },

  getTotal: () => {
    const { items } = get()
    return items.reduce((total, item) => total + item.discounted_price * item.quantity, 0)
  },
}))
