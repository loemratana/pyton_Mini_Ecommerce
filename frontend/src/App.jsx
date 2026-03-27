import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

// Pages
import { LoginPage, RegisterPage } from './pages/Auth'
import { AdminDashboard } from './pages/admin/Dashboard'
import { AdminProducts } from './pages/admin/Products'
import { AdminOrders } from './pages/admin/Orders'
import { AdminUsers } from './pages/admin/Users'
import { AdminAnalytics } from './pages/admin/Analytics'
import { AdminSettings } from './pages/admin/Settings'
import { AdminCategories } from './pages/admin/Categories'
import { CustomerDashboard } from './pages/customer/Dashboard'
import { CustomerShop } from './pages/customer/Shop'
import { CartPage } from './pages/customer/Cart'
import { CustomerOrders } from './pages/customer/Orders'
import { WishlistPage } from './pages/customer/Wishlist'
import { ProfilePage } from './pages/customer/Profile'

// Components
import { Header, AdminSidebar, CustomerSidebar } from './components/Layout'

// Store
import { useAuthStore } from './store/store'

// Protected Route Component
const ProtectedRoute = ({ children, requiredRole, allowGuest = false }) => {
  const { isAuthenticated, user } = useAuthStore()

  // 1. If allowGuest is true and user is NOT authenticated, allow access immediately
  if (allowGuest && !isAuthenticated) {
    return children
  }

  // 2. If user is NOT authenticated and it's NOT a guest route, redirect to login
  if (!isAuthenticated) {
    return <Navigate to='/login' replace />
  }

  // 3. If user is authenticated, check for role permissions
  if (requiredRole && user?.role !== requiredRole) {
    const target = user?.role === 'Admin' ? '/admin' : '/customer'
    // Prevent infinite redirect loops
    if (window.location.pathname === target) return children
    return <Navigate to={target} replace />
  }

  return children
}

const AdminLayout = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  return (
    <div className='flex flex-col h-screen bg-gray-50'>
      <Header
        toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        isSidebarOpen={isSidebarOpen}
      />
      <div className='flex flex-1 overflow-hidden'>
        <AdminSidebar
          isOpen={isSidebarOpen}
          closeSidebar={() => setIsSidebarOpen(false)}
        />
        <main className='flex-1 overflow-y-auto'>
          <div className='p-6 md:p-8'>{children}</div>
        </main>
      </div>
    </div>
  )
}

const CustomerLayout = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  return (
    <div className='flex flex-col h-screen bg-gray-50'>
      <Header
        toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        isSidebarOpen={isSidebarOpen}
      />
      <div className='flex flex-1 overflow-hidden'>
        <CustomerSidebar
          isOpen={isSidebarOpen}
          closeSidebar={() => setIsSidebarOpen(false)}
        />
        <main className='flex-1 overflow-y-auto'>
          <div className='p-6 md:p-8'>{children}</div>
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <>
      <Router future={{ v7_startTransition: true }}>
        <Routes>
          {/* Auth Routes */}
          <Route path='/login' element={<LoginPage />} />
          <Route path='/register' element={<RegisterPage />} />

          {/* Admin Routes */}
          <Route
            path='/admin'
            element={
              <ProtectedRoute requiredRole='Admin'>
                <AdminLayout>
                  <AdminDashboard />
                </AdminLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/admin/products'
            element={
              <ProtectedRoute requiredRole='Admin'>
                <AdminLayout>
                  <AdminProducts />
                </AdminLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/admin/categories'
            element={
              <ProtectedRoute requiredRole='Admin'>
                <AdminLayout>
                  <AdminCategories />
                </AdminLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/admin/orders'
            element={
              <ProtectedRoute requiredRole='Admin'>
                <AdminLayout>
                  <AdminOrders />
                </AdminLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/admin/users'
            element={
              <ProtectedRoute requiredRole='Admin'>
                <AdminLayout>
                  <AdminUsers />
                </AdminLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/admin/analytics'
            element={
              <ProtectedRoute requiredRole='Admin'>
                <AdminLayout>
                  <AdminAnalytics />
                </AdminLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/admin/settings'
            element={
              <ProtectedRoute requiredRole='Admin'>
                <AdminLayout>
                  <AdminSettings />
                </AdminLayout>
              </ProtectedRoute>
            }
          />

          {/* Customer Routes */}
          <Route
            path='/customer'
            element={
              <ProtectedRoute requiredRole='Customer' allowGuest={true}>
                <CustomerLayout>
                  <CustomerDashboard />
                </CustomerLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/customer/shop'
            element={
              <ProtectedRoute requiredRole='Customer' allowGuest={true}>
                <CustomerLayout>
                  <CustomerShop />
                </CustomerLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/customer/cart'
            element={
              <ProtectedRoute requiredRole='Customer'>
                <CustomerLayout>
                  <CartPage />
                </CustomerLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/customer/orders'
            element={
              <ProtectedRoute requiredRole='Customer'>
                <CustomerLayout>
                  <CustomerOrders />
                </CustomerLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/customer/wishlist'
            element={
              <ProtectedRoute requiredRole='Customer'>
                <CustomerLayout>
                  <WishlistPage />
                </CustomerLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path='/customer/profile'
            element={
              <ProtectedRoute requiredRole='Customer'>
                <CustomerLayout>
                  <ProfilePage />
                </CustomerLayout>
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path='/' element={<Navigate to='/customer' replace />} />
          <Route path='*' element={<Navigate to='/customer' replace />} />
        </Routes>
      </Router>

      <Toaster position='top-right' />
    </>
  )
}

export default App
