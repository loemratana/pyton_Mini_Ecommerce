import React, { useState } from 'react'
import { Card, Alert, Button, Modal } from '../../components/UI'
import { useAuthStore } from '../../store/store'
import { User, Mail, Shield, Edit2, LogOut, Lock, Phone, MapPin } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { apiService } from '../../services/apiService'
import toast from 'react-hot-toast'

export const ProfilePage = () => {
  const { user, updateUser, logout } = useAuthStore()
  const navigate = useNavigate()
  const [isEditOpen, setIsEditOpen] = useState(false)
  const [isPasswordOpen, setIsPasswordOpen] = useState(false)
  const [passwordLoading, setPasswordLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: user?.name || '',
    phone: user?.phone || '',
    address: user?.address || '',
  })
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  })

  const handleUpdateProfile = () => {
    if (!formData.name.trim()) {
      toast.error('Name is required')
      return
    }

    updateUser({
      ...user,
      name: formData.name,
      phone: formData.phone,
      address: formData.address,
    })

    toast.success('Profile updated successfully')
    setIsEditOpen(false)
  }

  const handleChangePassword = async () => {
    if (!passwordData.current_password || !passwordData.new_password) {
      toast.error('All fields are required')
      return
    }
    if (passwordData.new_password.length < 6) {
      toast.error('New password must be at least 6 characters')
      return
    }
    if (passwordData.new_password !== passwordData.confirm_password) {
      toast.error('Passwords do not match')
      return
    }

    setPasswordLoading(true)
    try {
      const res = await apiService.changePassword({
        current_password: passwordData.current_password,
        new_password: passwordData.new_password,
      })
      if (res.data.success) {
        toast.success('Password changed successfully')
        setIsPasswordOpen(false)
        setPasswordData({ current_password: '', new_password: '', confirm_password: '' })
      }
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to change password')
    } finally {
      setPasswordLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
    toast.success('Logged out successfully')
  }

  return (
    <div className='space-y-6'>
      <h1 className='text-3xl font-bold text-gray-900'>My Profile</h1>

      {/* Profile Card */}
      <Card>
        <div className='flex items-start justify-between mb-6'>
          <div className='flex items-start gap-6'>
            {/* Avatar */}
            <div className='w-24 h-24 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-3xl font-bold'>
              {user?.name?.charAt(0).toUpperCase()}
            </div>

            {/* Info */}
            <div>
              <h2 className='text-2xl font-bold text-gray-900'>{user?.name}</h2>
              <div className='flex items-center gap-2 mt-2'>
                <Shield className='w-4 h-4 text-blue-600' />
                <span className='text-sm text-gray-600 font-medium'>{user?.role}</span>
              </div>
              <div className='flex items-center gap-2 mt-2'>
                <Mail className='w-4 h-4 text-gray-600' />
                <span className='text-sm text-gray-600'>{user?.email}</span>
              </div>
            </div>
          </div>

          <Button
            variant='primary'
            onClick={() => setIsEditOpen(true)}
          >
            <Edit2 size={18} /> Edit Profile
          </Button>
        </div>
      </Card>

      {/* Account Details */}
      <Card>
        <h3 className='text-xl font-bold text-gray-900 mb-6'>Account Information</h3>

        <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
          <div className='p-4 bg-gray-50 rounded-lg'>
            <p className='text-sm text-gray-600 mb-1'>Full Name</p>
            <p className='font-semibold text-gray-900'>{user?.name}</p>
          </div>

          <div className='p-4 bg-gray-50 rounded-lg'>
            <p className='text-sm text-gray-600 mb-1'>Email Address</p>
            <p className='font-semibold text-gray-900'>{user?.email}</p>
          </div>

          <div className='p-4 bg-gray-50 rounded-lg'>
            <p className='text-sm text-gray-600 mb-1'>Account Type</p>
            <p className='font-semibold text-gray-900'>{user?.role} Account</p>
          </div>

          <div className='p-4 bg-gray-50 rounded-lg'>
            <p className='text-sm text-gray-600 mb-1'>User ID</p>
            <p className='font-semibold text-gray-900'>{user?.user_id}</p>
          </div>

          {user?.wishlist && (
            <div className='p-4 bg-gray-50 rounded-lg'>
              <p className='text-sm text-gray-600 mb-1'>Wishlist Items</p>
              <p className='font-semibold text-gray-900'>{user.wishlist.length} items</p>
            </div>
          )}

          <div className='p-4 bg-gray-50 rounded-lg'>
            <p className='text-sm text-gray-600 mb-1'>Account Status</p>
            <p className='font-semibold text-green-600'>Active</p>
          </div>
        </div>
      </Card>

      {/* Security Settings */}
      <Card>
        <h3 className='text-xl font-bold text-gray-900 mb-6'>Security</h3>

        <div className='space-y-4'>
          <div className='p-4 bg-blue-50 border border-blue-200 rounded-lg flex items-start justify-between'>
            <div>
              <p className='font-semibold text-gray-900'>Change Password</p>
              <p className='text-sm text-gray-600 mt-1'>Update your password regularly</p>
            </div>
            <Button variant='secondary' size='sm' onClick={() => setIsPasswordOpen(true)}>
              Change
            </Button>
          </div>

          <div className='p-4 bg-purple-50 border border-purple-200 rounded-lg flex items-start justify-between'>
            <div>
              <p className='font-semibold text-gray-900'>Two-Factor Authentication</p>
              <p className='text-sm text-gray-600 mt-1'>Add extra security to your account</p>
            </div>
            <Button variant='secondary' size='sm'>
              Enable
            </Button>
          </div>
        </div>
      </Card>

      {/* Danger Zone */}
      <Card>
        <h3 className='text-xl font-bold text-red-600 mb-6'>Danger Zone</h3>

        <div className='p-4 bg-red-50 border border-red-200 rounded-lg flex items-start justify-between'>
          <div>
            <p className='font-semibold text-gray-900'>Logout</p>
            <p className='text-sm text-gray-600 mt-1'>Sign out of your account</p>
          </div>
          <Button
            variant='danger'
            size='sm'
            onClick={handleLogout}
          >
            <LogOut size={18} /> Logout
          </Button>
        </div>
      </Card>

      {/* Edit Profile Modal */}
      <Modal
        isOpen={isEditOpen}
        title='Edit Profile'
        onClose={() => setIsEditOpen(false)}
        actions={[
          <Button key='cancel' variant='secondary' onClick={() => setIsEditOpen(false)}>
            Cancel
          </Button>,
          <Button key='save' variant='primary' onClick={handleUpdateProfile}>
            Save Changes
          </Button>,
        ]}
      >
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>Full Name</label>
            <input
              type='text'
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className='input'
              placeholder='Enter your name'
            />
          </div>

          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>Email Address</label>
            <input
              type='email'
              value={user?.email}
              disabled
              className='input opacity-50 cursor-not-allowed'
            />
            <p className='text-xs text-gray-500 mt-1'>Email cannot be changed</p>
          </div>

          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>Phone Number</label>
            <input
              type='tel'
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              className='input'
              placeholder='Enter your phone number'
            />
          </div>

          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>Address</label>
            <textarea
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              className='input'
              placeholder='Enter your address'
              rows='2'
            />
          </div>
        </div>
      </Modal>

      {/* Change Password Modal */}
      <Modal
        isOpen={isPasswordOpen}
        title='Change Password'
        onClose={() => setIsPasswordOpen(false)}
        actions={[
          <Button key='cancel' variant='secondary' onClick={() => setIsPasswordOpen(false)}>
            Cancel
          </Button>,
          <Button key='save' variant='primary' onClick={handleChangePassword} disabled={passwordLoading}>
            {passwordLoading ? 'Saving...' : 'Change Password'}
          </Button>,
        ]}
      >
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>Current Password</label>
            <input
              type='password'
              value={passwordData.current_password}
              onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
              className='input'
              placeholder='Enter current password'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>New Password</label>
            <input
              type='password'
              value={passwordData.new_password}
              onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
              className='input'
              placeholder='Enter new password (min 6 characters)'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>Confirm New Password</label>
            <input
              type='password'
              value={passwordData.confirm_password}
              onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
              className='input'
              placeholder='Confirm new password'
            />
          </div>
        </div>
      </Modal>
    </div>
  )
}
