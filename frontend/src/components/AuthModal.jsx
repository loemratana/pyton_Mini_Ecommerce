import React, { useState } from 'react'
import { Modal, Button, Alert, Spinner } from './UI'
import { Mail, Lock, User as UserIcon, X } from 'lucide-react'
import { apiService } from '../services/apiService'
import { useAuthStore } from '../store/store'
import toast from 'react-hot-toast'

export const AuthModal = ({ isOpen, onClose, onSuccess }) => {
  const [isLogin, setIsLogin] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuthStore()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    if (!isLogin && formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    setLoading(true)
    try {
      if (isLogin) {
        const response = await apiService.login({
          email: formData.email,
          password: formData.password
        })
        if (response.data.success) {
          login(response.data.user, response.data.token)
          toast.success('Login successful')
          onSuccess?.()
          onClose()
        }
      } else {
        const response = await apiService.register({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          role: 'Customer'
        })
        if (response.data.success) {
          login(response.data.user, response.data.token)
          toast.success('Registration successful! Welcome.')
          onSuccess?.()
          onClose()
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isLogin ? 'Login to Continue' : 'Create an Account'}
      size="md"
    >
      <div className="space-y-6">
        <div className="text-center mb-4">
          <p className="text-gray-500 text-sm">
            {isLogin 
              ? 'Please log in to add items to your cart.' 
              : 'Join us to start shopping and track your orders.'}
          </p>
        </div>

        {error && <Alert type="error" message={error} onClose={() => setError('')} />}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <div className="relative">
                <UserIcon className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="your@email.com"
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                required
              />
            </div>
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
            </div>
          )}

          <Button type="submit" variant="primary" className="w-full py-3" disabled={loading}>
            {loading ? <Spinner size="sm" className="mx-auto" /> : (isLogin ? 'Login' : 'Register')}
          </Button>
        </form>

        <div className="text-center pt-4 border-t border-gray-100">
          <p className="text-sm text-gray-600">
            {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-blue-600 font-semibold hover:underline"
            >
              {isLogin ? 'Register now' : 'Login here'}
            </button>
          </p>
        </div>
      </div>
    </Modal>
  )
}
