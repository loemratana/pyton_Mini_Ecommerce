import React, { useState, useEffect } from 'react'
import { Card, Alert, Spinner, Badge, Button, Modal } from '../../components/UI'
import { apiService } from '../../services/apiService'
import {
  Users, Mail, Shield, CheckCircle, AlertCircle,
  Search, Plus, Edit2, Trash2, ShieldAlert,
  ShieldCheck, UserPlus, MoreVertical, Calendar
} from 'lucide-react'
import toast from 'react-hot-toast'

export const AdminUsers = () => {
  const [users, setUsers] = useState([])
  const [filteredUsers, setFilteredUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  // Modal states
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'Customer',
    status: 'Active'
  })

  useEffect(() => {
    fetchUsers()
  }, [])

  useEffect(() => {
    filterUsers()
  }, [users, searchTerm])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await apiService.getUsers()
      if (response.data.success) {
        setUsers(response.data.users)
      }
    } catch (err) {
      setError('Failed to load users')
      toast.error('Failed to load users')
    } finally {
      setLoading(false)
    }
  }

  const filterUsers = () => {
    const filtered = users.filter(
      (user) =>
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase())
    )
    setFilteredUsers(filtered)
  }

  const handleOpenModal = (user = null) => {
    if (user) {
      setSelectedUser(user)
      setFormData({
        name: user.name,
        email: user.email,
        role: user.role,
        status: user.status || 'Active',
        password: ''
      })
    } else {
      setSelectedUser(null)
      setFormData({
        name: '',
        email: '',
        password: '',
        role: 'Customer',
        status: 'Active'
      })
    }
    setIsModalOpen(true)
  }

  const handleSaveUser = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      if (selectedUser) {
        const response = await apiService.updateUser(selectedUser.user_id, {
          name: formData.name,
          status: formData.status,
          role: formData.role
        })
        if (response.data.success) {
          toast.success('User updated successfully')
          fetchUsers()
          setIsModalOpen(false)
        }
      } else {
        const response = await apiService.register({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          role: formData.role
        })
        if (response.data.success) {
          toast.success('New user created successfully')
          fetchUsers()
          setIsModalOpen(false)
        }
      }
    } catch (err) {
      toast.error(err.response?.data?.message || 'Operation failed')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) return

    try {
      const response = await apiService.deleteUser(userId)
      if (response.data.success) {
        toast.success('User deleted successfully')
        fetchUsers()
      }
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to delete user')
    }
  }

  if (loading && users.length === 0) return <Spinner />

  const admins = filteredUsers.filter(u => u.role === 'Admin')
  const customers = filteredUsers.filter(u => u.role === 'Customer')

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex flex-col sm:flex-row sm:items-center justify-between gap-4'>
        <div>
          <h1 className='text-3xl font-bold text-gray-900'>Users Management</h1>
          <p className='text-gray-600 mt-1'>Manage admin and customer accounts</p>
        </div>
        <Button variant='primary' onClick={() => handleOpenModal()}>
          <UserPlus size={18} className='mr-2' />
          Add New User
        </Button>
      </div>

      {error && <Alert type='error' message={error} />}

      {/* Stats Summary */}
      <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4'>
        <StatCard
          icon={Users}
          label='Total Users'
          value={users.length}
        />
        <StatCard
          icon={ShieldCheck}
          label='Administrators'
          value={users.filter(u => u.role === 'Admin').length}
        />
        <StatCard
          icon={CheckCircle}
          label='Active Accounts'
          value={users.filter(u => u.status === 'Active').length}
        />
        <StatCard
          icon={Users}
          label='Customers'
          value={users.filter(u => u.role === 'Customer').length}
        />
      </div>

      {/* Search Bar */}
      <div className='relative'>
        <Search className='absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400' />
        <input
          type='text'
          placeholder='Search users by name or email...'
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className='w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
        />
      </div>

      {/* Admins Section */}
      <div>
        <div className='flex items-center gap-2 mb-4'>
          <Shield size={20} className='text-purple-600' />
          <h2 className='text-lg font-semibold text-gray-900'>Administrators</h2>
          <Badge variant='secondary' size='sm'>{admins.length}</Badge>
        </div>
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
          {admins.length > 0 ? (
            admins.map(user => (
              <UserCard
                key={user.user_id}
                user={user}
                onEdit={() => handleOpenModal(user)}
                onDelete={() => handleDeleteUser(user.user_id)}
              />
            ))
          ) : (
            <Card className='col-span-full text-center py-8'>
              <p className='text-gray-500'>No administrators found</p>
            </Card>
          )}
        </div>
      </div>

      {/* Customers Section */}
      <div>
        <div className='flex items-center gap-2 mb-4'>
          <Users size={20} className='text-blue-600' />
          <h2 className='text-lg font-semibold text-gray-900'>Customers</h2>
          <Badge variant='secondary' size='sm'>{customers.length}</Badge>
        </div>
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
          {customers.length > 0 ? (
            customers.map(user => (
              <UserCard
                key={user.user_id}
                user={user}
                onEdit={() => handleOpenModal(user)}
                onDelete={() => handleDeleteUser(user.user_id)}
              />
            ))
          ) : (
            <Card className='col-span-full text-center py-8'>
              <p className='text-gray-500'>No customers found</p>
            </Card>
          )}
        </div>
      </div>

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={selectedUser ? 'Edit User' : 'Add New User'}
        size='md'
        actions={[
          <Button key='cancel' variant='secondary' onClick={() => setIsModalOpen(false)}>
            Cancel
          </Button>,
          <Button key='save' variant='primary' onClick={handleSaveUser} disabled={submitting}>
            {submitting ? <Spinner size='sm' /> : (selectedUser ? 'Update User' : 'Create User')}
          </Button>
        ]}
      >
        <form className='space-y-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Full Name
            </label>
            <input
              type='text'
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Email Address
            </label>
            <input
              type='email'
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              disabled={!!selectedUser}
            />
          </div>
          {!selectedUser && (
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Password
              </label>
              <input
                type='password'
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
              />
            </div>
          )}
          <div className='grid grid-cols-2 gap-4'>
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Role
              </label>
              <select
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white'
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              >
                <option value='Customer'>Customer</option>
                <option value='Admin'>Admin</option>
              </select>
            </div>
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Status
              </label>
              <select
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white'
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <option value='Active'>Active</option>
                <option value='Suspended'>Suspended</option>
                <option value='Pending'>Pending</option>
              </select>
            </div>
          </div>
        </form>
      </Modal>
    </div>
  )
}

const StatCard = ({ icon: Icon, label, value }) => (
  <Card className='p-4'>
    <div className='flex items-center gap-4'>
      <div className='w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center'>
        <Icon size={20} className='text-gray-600' />
      </div>
      <div>
        <p className='text-sm text-gray-500'>{label}</p>
        <p className='text-2xl font-semibold text-gray-900'>{value}</p>
      </div>
    </div>
  </Card>
)

const UserCard = ({ user, onEdit, onDelete }) => {
  const isAdmin = user.role === 'Admin'
  const isActive = user.status === 'Active'

  return (
    <Card className='p-4 hover:shadow-md transition-shadow'>
      <div className='flex items-start justify-between mb-3'>
        <div className='flex items-center gap-3'>
          <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium ${isAdmin ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700'
            }`}>
            {user.name?.charAt(0).toUpperCase()}
          </div>
          <div>
            <h3 className='font-medium text-gray-900'>{user.name}</h3>
            <p className='text-xs text-gray-500 flex items-center gap-1 mt-0.5'>
              <Mail size={12} />
              {user.email}
            </p>
          </div>
        </div>
        <Badge variant={isAdmin ? 'danger' : 'primary'}>
          {user.role}
        </Badge>
      </div>

      <div className='space-y-2 text-sm mt-3 pt-3 border-t border-gray-100'>
        <div className='flex items-center justify-between'>
          <span className='text-gray-500'>Status:</span>
          <div className='flex items-center gap-1'>
            <span className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-500' : 'bg-red-500'}`}></span>
            <span className={`text-sm ${isActive ? 'text-green-600' : 'text-red-600'}`}>
              {user.status}
            </span>
          </div>
        </div>
        <div className='flex items-center justify-between'>
          <span className='text-gray-500'>Joined:</span>
          <span className='text-gray-700 text-sm'>
            {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
          </span>
        </div>
        <div className='flex items-center justify-between'>
          <span className='text-gray-500'>Wishlist:</span>
          <span className='text-gray-700 text-sm font-medium'>{user.wishlist_count || 0} items</span>
        </div>
      </div>

      <div className='mt-3 pt-3 border-t border-gray-100 flex justify-end gap-2'>
        <button
          onClick={onEdit}
          className='p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors'
          title='Edit'
        >
          <Edit2 size={16} />
        </button>
        <button
          onClick={onDelete}
          className='p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors'
          title='Delete'
        >
          <Trash2 size={16} />
        </button>
      </div>
    </Card>
  )
}