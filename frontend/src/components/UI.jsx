import React from 'react'
import { AlertCircle, CheckCircle, InfoIcon, AlertTriangle } from 'lucide-react'

export const Alert = ({ type = 'info', title, message, onClose }) => {
  const config = {
    success: { bg: 'bg-green-50', border: 'border-green-200', icon: CheckCircle, text: 'text-green-800' },
    error: { bg: 'bg-red-50', border: 'border-red-200', icon: AlertCircle, text: 'text-red-800' },
    warning: { bg: 'bg-yellow-50', border: 'border-yellow-200', icon: AlertTriangle, text: 'text-yellow-800' },
    info: { bg: 'bg-blue-50', border: 'border-blue-200', icon: InfoIcon, text: 'text-blue-800' },
  }

  const { bg, border, icon: Icon, text } = config[type]

  return (
    <div className={`${bg} border ${border} rounded-lg p-4 flex items-start gap-3 animate-slideUp`}>
      <Icon className={`w-5 h-5 ${text} flex-shrink-0 mt-0.5`} />
      <div className='flex-1'>
        {title && <h3 className={`font-semibold ${text}`}>{title}</h3>}
        <p className={`text-sm ${text} opacity-90`}>{message}</p>
      </div>
      {onClose && (
        <button onClick={onClose} className={`${text} hover:opacity-70`}>
          ×
        </button>
      )}
    </div>
  )
}

export const Spinner = ({ size = 'md', className = '' }) => {
  const sizeClass = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }[size]

  return (
    <div className={`${sizeClass} border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin ${className}`} />
  )
}

export const LoadingPage = () => (
  <div className='flex items-center justify-center min-h-screen'>
    <div className='text-center'>
      <Spinner size='lg' className='mx-auto mb-4' />
      <p className='text-gray-600'>Loading...</p>
    </div>
  </div>
)

export const Card = ({ children, className = '', ...props }) => (
  <div className={`card ${className}`} {...props}>
    {children}
  </div>
)

export const Button = ({ children, variant = 'primary', size = 'md', disabled = false, className = '', ...props }) => {
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    danger: 'btn-danger',
    success: 'btn-success',
  }

  const sizes = {
    sm: 'text-sm px-3 py-1',
    md: 'text-base px-4 py-2',
    lg: 'text-lg px-6 py-3',
  }

  return (
    <button
      className={`${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  )
}

export const Badge = ({ children, variant = 'primary', className = '' }) => {
  const variants = {
    primary: 'badge-primary',
    success: 'badge-success',
    warning: 'badge-warning',
    danger: 'badge-danger',
  }

  return <span className={`${variants[variant]} ${className}`}>{children}</span>
}

export const Modal = ({ isOpen, title, children, onClose, actions, size = 'md' }) => {
  if (!isOpen) return null

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
    '3xl': 'max-w-3xl',
  }

  return (
    <div className='fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto animate-fadeIn'>
      <div className={`bg-white rounded-xl shadow-xl ${sizeClasses[size] || sizeClasses.md} w-full animate-slideUp my-auto`}>
        <div className='p-6 border-b border-gray-100 flex items-center justify-between bg-gray-50 rounded-t-xl'>
          <h2 className='text-xl font-bold text-gray-800'>{title}</h2>
          <button onClick={onClose} className='p-2 hover:bg-gray-200 rounded-full transition text-gray-400 hover:text-gray-600'>
            <span className='text-2xl leading-none'>&times;</span>
          </button>
        </div>
        <div className='p-8 max-h-[70vh] overflow-y-auto custom-scrollbar'>{children}</div>
        {actions && (
          <div className='p-6 border-t border-gray-100 flex gap-3 justify-end bg-gray-50 rounded-b-xl'>
            {actions}
          </div>
        )}
      </div>
    </div>
  )
}

export const SearchInput = ({ placeholder = 'Search...', onSearch, className = '' }) => (
  <input
    type='text'
    placeholder={placeholder}
    onChange={(e) => onSearch(e.target.value)}
    className={`input ${className}`}
  />
)
