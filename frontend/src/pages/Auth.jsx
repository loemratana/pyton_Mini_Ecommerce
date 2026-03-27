import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { apiService } from '../services/apiService'
import { useAuthStore } from '../store/store'
import { Alert, Button, Spinner } from '../components/UI'
import { Mail, Lock, User as UserIcon, Eye, EyeOff, ShoppingBag, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'
import { LanguageSwitcher } from '../components/LanguageSwitcher'

export const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { login } = useAuthStore()

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await apiService.login({ email, password })
      if (response.data.success) {
        login(response.data.user, response.data.token)
        toast.success('Login successful! Welcome back.')

        if (response.data.user.role === 'Admin') {
          navigate('/admin')
        } else {
          navigate('/customer')
        }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Invalid email or password. Please try again.'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const fillDemoCredentials = (type) => {
    if (type === 'admin') {
      setEmail('admin@shop.com')
      setPassword('admin')
    } else {
      setEmail('john@example.com')
      setPassword('user123')
    }
  }

  return (
    <div className='min-h-screen bg-gray-50 flex items-center justify-center p-4 relative'>
      <div className='absolute top-4 right-4'>
        <LanguageSwitcher />
      </div>
      <div className='w-full max-w-md'>
        {/* Logo & Brand */}
        <div className='text-center mb-8'>
          <div className='inline-flex items-center justify-center w-16 h-16 bg-gray-900 rounded-2xl mb-4 shadow-lg'>
            <ShoppingBag className='w-8 h-8 text-white' />
          </div>
          <h1 className='text-3xl font-bold text-gray-900'>Antigravity</h1>
          <p className='text-gray-500 mt-1'>Sign in to your account</p>
        </div>

        {/* Login Form */}
        <div className='bg-white rounded-xl shadow-sm border border-gray-100 p-8'>
          <h2 className='text-xl font-semibold text-gray-900 mb-6'>Welcome Back</h2>

          {error && (
            <Alert type='error' message={error} onClose={() => setError('')} className='mb-4' />
          )}

          <form onSubmit={handleLogin} className='space-y-4'>
            {/* Email */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Email Address</label>
              <div className='relative'>
                <Mail className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
                <input
                  type='email'
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder='your@email.com'
                  className='w-full pl-9 pr-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-gray-400'
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Password</label>
              <div className='relative'>
                <Lock className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder='••••••••'
                  className='w-full pl-9 pr-9 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-gray-400'
                  required
                  disabled={loading}
                />
                <button
                  type='button'
                  onClick={() => setShowPassword(!showPassword)}
                  className='absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600'
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <Button type='submit' variant='primary' className='w-full' disabled={loading}>
              {loading ? (
                <Spinner size='sm' />
              ) : (
                <>
                  Sign In
                  <ArrowRight size={16} className='ml-2' />
                </>
              )}
            </Button>
          </form>

          {/* Register Link */}
          <div className='mt-6 text-center text-sm text-gray-500'>
            Don't have an account?{' '}
            <Link to='/register' className='text-gray-900 font-medium hover:underline'>
              Create account
            </Link>
          </div>
        </div>

        {/* Demo Credentials */}
        <div className='mt-6 bg-white rounded-lg border border-gray-100 p-4'>
          <p className='text-xs font-medium text-gray-500 uppercase tracking-wider mb-2'>Demo Credentials</p>
          <div className='space-y-2 text-sm'>
            <button
              onClick={() => fillDemoCredentials('admin')}
              className='w-full text-left px-3 py-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors'
            >
              <span className='font-medium text-gray-900'>Admin:</span>{' '}
              <span className='text-gray-600'>admin@shop.com / admin</span>
            </button>
            <button
              onClick={() => fillDemoCredentials('customer')}
              className='w-full text-left px-3 py-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors'
            >
              <span className='font-medium text-gray-900'>Customer:</span>{' '}
              <span className='text-gray-600'>john@example.com / user123</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export const RegisterPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'Customer',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { login } = useAuthStore()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setError('')

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    setLoading(true)

    try {
      const response = await apiService.register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        role: formData.role,
      })

      if (response.data.success) {
        login(response.data.user, response.data.token)
        toast.success('Registration successful! Welcome to Antigravity.')

        if (response.data.user.role === 'Admin') {
          navigate('/admin')
        } else {
          navigate('/customer')
        }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Registration failed. Please try again.'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='min-h-screen bg-gray-50 flex items-center justify-center p-4 relative'>
      <div className='absolute top-4 right-4'>
        <LanguageSwitcher />
      </div>
      <div className='w-full max-w-md'>
        {/* Logo & Brand */}
        <div className='text-center mb-8'>
          <div className='inline-flex items-center justify-center w-16 h-16 bg-gray-900 rounded-2xl mb-4 shadow-lg'>
            <ShoppingBag className='w-8 h-8 text-white' />
          </div>
          <h1 className='text-3xl font-bold text-gray-900'>Antigravity</h1>
          <p className='text-gray-500 mt-1'>Create your account</p>
        </div>

        {/* Register Form */}
        <div className='bg-white rounded-xl shadow-sm border border-gray-100 p-8'>
          <h2 className='text-xl font-semibold text-gray-900 mb-6'>Get Started</h2>

          {error && (
            <Alert type='error' message={error} onClose={() => setError('')} className='mb-4' />
          )}

          <form onSubmit={handleRegister} className='space-y-4'>
            {/* Full Name */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Full Name</label>
              <div className='relative'>
                <UserIcon className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
                <input
                  type='text'
                  name='name'
                  value={formData.name}
                  onChange={handleChange}
                  placeholder='John Doe'
                  className='w-full pl-9 pr-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-gray-400'
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Email Address</label>
              <div className='relative'>
                <Mail className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
                <input
                  type='email'
                  name='email'
                  value={formData.email}
                  onChange={handleChange}
                  placeholder='your@email.com'
                  className='w-full pl-9 pr-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-gray-400'
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Role */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Account Type</label>
              <select
                name='role'
                value={formData.role}
                onChange={handleChange}
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-gray-400 bg-white'
                disabled={loading}
              >
                <option value='Customer'>Customer - Shop and purchase products</option>
                <option value='Admin'>Admin - Manage store and inventory</option>
              </select>
            </div>

            {/* Password */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Password</label>
              <div className='relative'>
                <Lock className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name='password'
                  value={formData.password}
                  onChange={handleChange}
                  placeholder='••••••••'
                  className='w-full pl-9 pr-9 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-gray-400'
                  required
                  disabled={loading}
                />
                <button
                  type='button'
                  onClick={() => setShowPassword(!showPassword)}
                  className='absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600'
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              <p className='text-xs text-gray-400 mt-1'>At least 6 characters</p>
            </div>

            {/* Confirm Password */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Confirm Password</label>
              <div className='relative'>
                <Lock className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  name='confirmPassword'
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder='••••••••'
                  className='w-full pl-9 pr-9 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-gray-400'
                  required
                  disabled={loading}
                />
                <button
                  type='button'
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className='absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600'
                >
                  {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <Button type='submit' variant='primary' className='w-full' disabled={loading}>
              {loading ? (
                <Spinner size='sm' />
              ) : (
                <>
                  Create Account
                  <ArrowRight size={16} className='ml-2' />
                </>
              )}
            </Button>
          </form>

          {/* Login Link */}
          <div className='mt-6 text-center text-sm text-gray-500'>
            Already have an account?{' '}
            <Link to='/login' className='text-gray-900 font-medium hover:underline'>
              Sign in
            </Link>
          </div>
        </div>

        {/* Terms Notice */}
        <p className='text-center text-xs text-gray-400 mt-6'>
          By creating an account, you agree to our{' '}
          <a href='#' className='text-gray-500 hover:underline'>Terms of Service</a>{' '}
          and{' '}
          <a href='#' className='text-gray-500 hover:underline'>Privacy Policy</a>
        </p>
      </div>
    </div>
  )
}