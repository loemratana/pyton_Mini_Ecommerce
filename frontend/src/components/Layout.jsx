import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { LogOut, Menu, X, User, Home, ShoppingBag, Users, BarChart3, Settings, FolderOpen, Layers, Heart } from 'lucide-react'
import { useAuthStore } from '../store/store'
import { LanguageSwitcher } from './LanguageSwitcher'

export const Header = ({ toggleSidebar, isSidebarOpen }) => {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className='bg-white border-b border-gray-200 sticky top-0 z-30'>
      <div className='flex items-center justify-between h-16 px-6'>
        <div className='flex items-center gap-4'>
          <button
            onClick={toggleSidebar}
            className='lg:hidden text-gray-500 hover:text-gray-700 transition-colors'
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <Link to={user?.role === 'admin' ? '/admin' : '/customer'} className='flex items-center gap-2'>
            <div className='w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center'>
              <span className='text-white font-semibold text-sm'>A</span>
            </div>
            <span className='font-semibold text-gray-900'>Antigravity</span>
          </Link>
        </div>

        <div className='flex items-center gap-4'>
          <div className='flex items-center gap-3'>
            <div className='w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center'>
              <User size={16} className='text-gray-600' />
            </div>
            <div className='hidden sm:block'>
              <p className='text-sm font-medium text-gray-900'>{user?.name || 'User'}</p>
              <p className='text-xs text-gray-500 capitalize'>{user?.role || 'customer'}</p>
            </div>
          </div>

          <div className="h-6 w-px bg-gray-200 hidden sm:block"></div>
          
          <LanguageSwitcher />

          <button
            onClick={handleLogout}
            className='p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors'
            title='Logout'
          >
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </header>
  )
}

export const AdminSidebar = ({ isOpen, closeSidebar }) => {
  const location = useLocation()

  const navItems = [
    { path: '/admin', icon: Home, label: 'Dashboard' },
    { path: '/admin/products', icon: ShoppingBag, label: 'Products' },
    { path: '/admin/categories', icon: Layers, label: 'Categories' },
    { path: '/admin/orders', icon: FolderOpen, label: 'Orders' },
    { path: '/admin/users', icon: Users, label: 'Users' },
    { path: '/admin/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/admin/settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className='fixed inset-0 bg-black/50 z-20 lg:hidden'
          onClick={closeSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed left-0 top-16 w-64 h-[calc(100vh-64px)] bg-white border-r border-gray-200 
          transform transition-transform duration-300 ease-in-out z-30
          lg:relative lg:top-0 lg:translate-x-0 lg:z-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <nav className='p-4 space-y-1'>
          {navItems.map(({ path, icon: Icon, label }) => {
            const isActive = location.pathname === path
            return (
              <Link
                key={path}
                to={path}
                onClick={closeSidebar}
                className={`
                  flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200
                  ${isActive
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                  }
                `}
              >
                <Icon size={18} />
                <span className='text-sm font-medium'>{label}</span>
              </Link>
            )
          })}
        </nav>
      </aside>
    </>
  )
}

export const CustomerSidebar = ({ isOpen, closeSidebar }) => {
  const location = useLocation()
  const { user } = useAuthStore()

  const navItems = [
    { path: '/customer', icon: Home, label: 'Dashboard' },
    { path: '/customer/shop', icon: ShoppingBag, label: 'Shop' },
  ]

  // Add protected items only if logged in
  if (user) {
    navItems.push(
      { path: '/customer/cart', icon: ShoppingBag, label: 'Cart' },
      { path: '/customer/orders', icon: FolderOpen, label: 'Orders' },
      { path: '/customer/wishlist', icon: Heart, label: 'Wishlist' },
      { path: '/customer/profile', icon: User, label: 'Profile' }
    )
  } else {
    // Add Login link for guests
    navItems.unshift({ path: '/login', icon: LogOut, label: 'Login / Register' })
  }

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className='fixed inset-0 bg-black/50 z-20 lg:hidden'
          onClick={closeSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed left-0 top-16 w-64 h-[calc(100vh-64px)] bg-white border-r border-gray-200 
          transform transition-transform duration-300 ease-in-out z-30
          lg:relative lg:top-0 lg:translate-x-0 lg:z-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        {/* User Info */}
        <div className='p-4 border-b border-gray-100 mb-2'>
          <div className='flex items-center gap-3'>
            <div className='w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center'>
              <User size={20} className='text-gray-600' />
            </div>
            <div>
              <p className='text-sm font-medium text-gray-900'>{user?.name || 'Guest'}</p>
              <p className='text-xs text-gray-500'>{user?.email || 'Not signed in'}</p>
            </div>
          </div>
        </div>

        <nav className='p-4 space-y-1'>
          {navItems.map(({ path, icon: Icon, label }) => {
            const isActive = location.pathname === path
            return (
              <Link
                key={path}
                to={path}
                onClick={closeSidebar}
                className={`
                  flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200
                  ${isActive
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                  }
                `}
              >
                <Icon size={18} />
                <span className='text-sm font-medium'>{label}</span>
              </Link>
            )
          })}
        </nav>
      </aside>
    </>
  )
}