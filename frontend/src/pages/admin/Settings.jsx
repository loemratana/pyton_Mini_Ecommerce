import React, { useState, useEffect } from 'react'
import { Card, Button, Alert, Spinner, Badge } from '../../components/UI'
import {
  Settings, Download, RotateCcw, Package,
  Mail, Phone, MapPin, Globe, Shield, Database,
  Bell, CreditCard, Truck, DollarSign, Users,
  RefreshCw, CheckCircle, XCircle, AlertCircle
} from 'lucide-react'
import { apiService } from '../../services/apiService'
import toast from 'react-hot-toast'

export const AdminSettings = () => {
  const [loading, setLoading] = useState(false)
  const [storeSettings, setStoreSettings] = useState({
    storeName: 'Antigravity Store',
    storeEmail: 'store@antigravity.com',
    supportEmail: 'support@antigravity.com',
    phone: '+1 (800) 555-0123',
    address: '123 Innovation Drive, Silicon Valley, CA 94025',
    currency: 'USD',
    taxRate: 8.5,
    shippingCost: 5.99,
    freeShippingThreshold: 50
  })

  const [systemInfo, setSystemInfo] = useState({
    apiVersion: '1.0.0',
    frontendVersion: '1.0.0',
    lastBackup: 'Today at 12:00 AM',
    databaseSize: '2.4 MB',
    totalOrders: 0,
    totalProducts: 0,
    totalUsers: 0
  })

  useEffect(() => {
    fetchSystemInfo()
  }, [])

  const fetchSystemInfo = async () => {
    try {
      const [ordersRes, productsRes, usersRes] = await Promise.all([
        apiService.getOrders(),
        apiService.getProducts(),
        apiService.getUsers()
      ])

      setSystemInfo(prev => ({
        ...prev,
        totalOrders: ordersRes.data?.orders?.length || 0,
        totalProducts: productsRes.data?.products?.length || 0,
        totalUsers: usersRes.data?.users?.length || 0
      }))
    } catch (err) {
      console.error('Failed to fetch system info')
    }
  }

  const handleSaveSettings = async () => {
    setLoading(true)
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      localStorage.setItem('storeSettings', JSON.stringify(storeSettings))
      toast.success('Settings saved successfully')
    } catch (err) {
      toast.error('Failed to save settings')
    } finally {
      setLoading(false)
    }
  }

  const handleDatabaseBackup = async () => {
    setLoading(true)
    try {
      const response = await apiService.backupDatabase()
      if (response.data.success) {
        toast.success('Database backup initiated successfully')
      }
    } catch (err) {
      toast.error('Failed to backup database')
    } finally {
      setLoading(false)
    }
  }

  const handleExportData = () => {
    const exportData = {
      exportDate: new Date().toISOString(),
      store: storeSettings,
      system: systemInfo,
      timestamp: Date.now()
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const element = document.createElement('a')
    element.setAttribute('href', url)
    element.setAttribute('download', `store-backup-${new Date().toISOString().split('T')[0]}.json`)
    element.style.display = 'none'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
    URL.revokeObjectURL(url)
    toast.success('Data exported successfully')
  }

  const handleClearCache = () => {
    localStorage.removeItem('storeSettings')
    sessionStorage.clear()
    toast.success('Cache cleared successfully')
  }

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div>
        <h1 className='text-2xl font-semibold text-gray-900'>Settings</h1>
        <p className='text-gray-500 mt-1'>Manage your store configuration and maintenance</p>
      </div>

      {/* Store Settings */}
      <Card className='p-6'>
        <div className='flex items-center gap-2 mb-6'>
          <Settings size={20} className='text-gray-600' />
          <h2 className='text-lg font-semibold text-gray-900'>Store Information</h2>
        </div>

        <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Store Name</label>
            <input
              type='text'
              value={storeSettings.storeName}
              onChange={(e) => setStoreSettings({ ...storeSettings, storeName: e.target.value })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Store Email</label>
            <input
              type='email'
              value={storeSettings.storeEmail}
              onChange={(e) => setStoreSettings({ ...storeSettings, storeEmail: e.target.value })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Support Email</label>
            <input
              type='email'
              value={storeSettings.supportEmail}
              onChange={(e) => setStoreSettings({ ...storeSettings, supportEmail: e.target.value })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Phone Number</label>
            <input
              type='tel'
              value={storeSettings.phone}
              onChange={(e) => setStoreSettings({ ...storeSettings, phone: e.target.value })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
            />
          </div>
          <div className='md:col-span-2'>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Store Address</label>
            <textarea
              value={storeSettings.address}
              onChange={(e) => setStoreSettings({ ...storeSettings, address: e.target.value })}
              rows={2}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 resize-none'
            />
          </div>
        </div>

        <div className='mt-6'>
          <Button variant='primary' onClick={handleSaveSettings} disabled={loading}>
            {loading ? <Spinner size='sm' /> : 'Save Settings'}
          </Button>
        </div>
      </Card>

      {/* Shipping & Tax Settings */}
      <Card className='p-6'>
        <div className='flex items-center gap-2 mb-6'>
          <Truck size={20} className='text-gray-600' />
          <h2 className='text-lg font-semibold text-gray-900'>Shipping & Tax</h2>
        </div>

        <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Currency</label>
            <select
              value={storeSettings.currency}
              onChange={(e) => setStoreSettings({ ...storeSettings, currency: e.target.value })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white'
            >
              <option value='USD'>USD ($)</option>
              <option value='EUR'>EUR (€)</option>
              <option value='GBP'>GBP (£)</option>
              <option value='CAD'>CAD ($)</option>
            </select>
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Tax Rate (%)</label>
            <input
              type='number'
              step='0.1'
              value={storeSettings.taxRate}
              onChange={(e) => setStoreSettings({ ...storeSettings, taxRate: parseFloat(e.target.value) })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Default Shipping ($)</label>
            <input
              type='number'
              step='0.01'
              value={storeSettings.shippingCost}
              onChange={(e) => setStoreSettings({ ...storeSettings, shippingCost: parseFloat(e.target.value) })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
            />
          </div>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-1'>Free Shipping Threshold ($)</label>
            <input
              type='number'
              step='0.01'
              value={storeSettings.freeShippingThreshold}
              onChange={(e) => setStoreSettings({ ...storeSettings, freeShippingThreshold: parseFloat(e.target.value) })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
            />
          </div>
        </div>
      </Card>

      {/* Maintenance */}
      <Card className='p-6'>
        <div className='flex items-center gap-2 mb-6'>
          <Database size={20} className='text-gray-600' />
          <h2 className='text-lg font-semibold text-gray-900'>Maintenance</h2>
        </div>

        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3'>
          <Button variant='secondary' onClick={handleDatabaseBackup} className='gap-2'>
            <Download size={16} />
            Backup Database
          </Button>
          <Button variant='secondary' onClick={handleExportData} className='gap-2'>
            <Package size={16} />
            Export All Data
          </Button>
          <Button variant='secondary' onClick={handleClearCache} className='gap-2'>
            <RefreshCw size={16} />
            Clear Cache
          </Button>
          <Button variant='danger' className='gap-2'>
            <RotateCcw size={16} />
            Reset Analytics
          </Button>
        </div>
      </Card>

      {/* System Information */}
      <Card className='p-6'>
        <div className='flex items-center gap-2 mb-6'>
          <Shield size={20} className='text-gray-600' />
          <h2 className='text-lg font-semibold text-gray-900'>System Information</h2>
        </div>

        <div className='grid grid-cols-2 md:grid-cols-4 gap-4'>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>API Version</p>
            <p className='font-semibold text-gray-900'>{systemInfo.apiVersion}</p>
          </div>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>Frontend Version</p>
            <p className='font-semibold text-gray-900'>{systemInfo.frontendVersion}</p>
          </div>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>Last Backup</p>
            <p className='font-semibold text-gray-900'>{systemInfo.lastBackup}</p>
          </div>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>Database Size</p>
            <p className='font-semibold text-gray-900'>{systemInfo.databaseSize}</p>
          </div>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>Total Orders</p>
            <p className='font-semibold text-gray-900'>{systemInfo.totalOrders}</p>
          </div>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>Total Products</p>
            <p className='font-semibold text-gray-900'>{systemInfo.totalProducts}</p>
          </div>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>Total Users</p>
            <p className='font-semibold text-gray-900'>{systemInfo.totalUsers}</p>
          </div>
          <div className='p-3 bg-gray-50 rounded-lg'>
            <p className='text-xs text-gray-500'>Environment</p>
            <Badge variant='success' size='sm'>Production</Badge>
          </div>
        </div>
      </Card>

      {/* Quick Actions */}
      <Card className='p-6'>
        <div className='flex items-center gap-2 mb-6'>
          <Bell size={20} className='text-gray-600' />
          <h2 className='text-lg font-semibold text-gray-900'>Quick Actions</h2>
        </div>

        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3'>
          <Button variant='secondary' className='justify-start gap-2'>
            <Mail size={16} />
            Test Email System
          </Button>
          <Button variant='secondary' className='justify-start gap-2'>
            <Globe size={16} />
            Clear Store Cache
          </Button>
          <Button variant='secondary' className='justify-start gap-2'>
            <Users size={16} />
            Send Newsletter
          </Button>
        </div>
      </Card>

      {/* Important Notice */}
      <Alert
        type='info'
        title='Important Notice'
        message='Please perform regular backups to prevent data loss. We recommend backing up your database at least once a week.'
      />
    </div>
  )
}