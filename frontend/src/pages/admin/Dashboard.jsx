import React, { useState, useEffect } from 'react'
import { Card, Alert, Spinner, Button, Badge } from '../../components/UI'
import { apiService } from '../../services/apiService'
import { BarChart3, ShoppingBag, Users, DollarSign, TrendingUp, Package, Eye, PlusCircle, AlertCircle } from 'lucide-react'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'

export const AdminDashboard = () => {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true)
        const response = await apiService.getDashboardAnalytics()
        if (response.data.success) {
          setAnalytics(response.data.analytics)
        }
      } catch (err) {
        const message = err.response?.data?.message || 'Failed to load analytics'
        setError(message)
        toast.error(message)
      } finally {
        setLoading(false)
      }
    }

    fetchAnalytics()
  }, [])

  if (loading) return <Spinner />

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='bg-white border border-gray-100 rounded-lg p-6'>
        <h1 className='text-2xl font-semibold text-gray-900 mb-1'>Admin Dashboard</h1>
        <p className='text-gray-500'>Welcome back! Here's your store overview.</p>
      </div>

      {error && <Alert type='error' message={error} />}

      {/* KPI Cards */}
      {analytics && (
        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4'>
          <KPICard
            icon={DollarSign}
            label='Total Revenue'
            value={`$${analytics.total_revenue.toFixed(2)}`}
          />
          <KPICard
            icon={ShoppingBag}
            label='Total Orders'
            value={analytics.total_orders}
          />
          <KPICard
            icon={Package}
            label='Total Products'
            value={analytics.total_products}
          />
          <KPICard
            icon={Users}
            label='Total Customers'
            value={analytics.total_customers}
          />
        </div>
      )}

      {/* Charts Row */}
      {analytics && (
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/* Orders by Status */}
          <Card className='p-6'>
            <div className='flex items-center justify-between mb-4'>
              <h3 className='text-lg font-semibold text-gray-900 flex items-center gap-2'>
                <BarChart3 size={18} className='text-gray-600' />
                Orders by Status
              </h3>
              <Link to='/admin/orders' className='text-sm text-blue-600 hover:text-blue-700'>
                View All →
              </Link>
            </div>
            <div className='space-y-4'>
              {Object.entries(analytics.status_breakdown).map(([status, count]) => {
                const percentage = (count / analytics.total_orders) * 100
                return (
                  <div key={status}>
                    <div className='flex items-center justify-between mb-1'>
                      <span className='text-sm text-gray-600 capitalize'>{status}</span>
                      <div className='flex items-center gap-2'>
                        <span className='text-sm font-medium text-gray-900'>{count}</span>
                        <span className='text-xs text-gray-400'>({percentage.toFixed(1)}%)</span>
                      </div>
                    </div>
                    <div className='w-full bg-gray-100 rounded-full h-2'>
                      <div
                        className='bg-gray-900 h-2 rounded-full transition-all duration-500'
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </Card>

          {/* Top Products */}
          <Card className='p-6'>
            <div className='flex items-center justify-between mb-4'>
              <h3 className='text-lg font-semibold text-gray-900 flex items-center gap-2'>
                <TrendingUp size={18} className='text-gray-600' />
                Top Selling Products
              </h3>
              <Link to='/admin/products' className='text-sm text-blue-600 hover:text-blue-700'>
                Manage →
              </Link>
            </div>
            <div className='space-y-3'>
              {analytics.top_products && analytics.top_products.length > 0 ? (
                analytics.top_products.slice(0, 5).map(([productId, name, sales], index) => (
                  <div key={productId} className='flex items-center justify-between py-2 border-b border-gray-100 last:border-0'>
                    <div className='flex items-center gap-3'>
                      <div className='w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center text-xs font-medium text-gray-600'>
                        {index + 1}
                      </div>
                      <div>
                        <p className='text-sm font-medium text-gray-900'>{name}</p>
                        <p className='text-xs text-gray-400'>ID: {productId}</p>
                      </div>
                    </div>
                    <div className='text-right'>
                      <p className='text-sm font-semibold text-gray-900'>{sales} sold</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className='text-center py-8'>
                  <Package size={32} className='text-gray-300 mx-auto mb-2' />
                  <p className='text-sm text-gray-500'>No sales data yet</p>
                </div>
              )}
            </div>
          </Card>
        </div>
      )}

      {/* Low Stock Alerts */}
      {analytics?.low_stock_alerts?.length > 0 && (
        <Card className='p-6 border-orange-100 bg-orange-50/20'>
          <h3 className='text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2'>
            <AlertCircle size={18} className='text-orange-600' />
            Inventory Alerts
          </h3>
          <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3'>
            {analytics.low_stock_alerts.map((alert) => (
              <div key={alert.product_id} className='bg-white p-3 rounded-lg border border-orange-100 flex items-center justify-between'>
                <div>
                  <p className='text-sm font-medium text-gray-900'>{alert.name}</p>
                  <p className='text-xs text-gray-500'>ID: {alert.product_id}</p>
                </div>
                <Badge variant='danger' className='bg-red-100 text-red-700 border-red-200'>
                  {alert.stock} left
                </Badge>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Quick Actions */}
      <Card className='p-6'>
        <h3 className='text-lg font-semibold text-gray-900 mb-4'>Quick Actions</h3>
        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3'>
          <Link to='/admin/products'>
            <Button variant='primary' className='w-full gap-2'>
              <PlusCircle size={16} />
              Add Product
            </Button>
          </Link>
          <Link to='/admin/orders'>
            <Button variant='secondary' className='w-full gap-2'>
              <Eye size={16} />
              View Orders
            </Button>
          </Link>
          <Link to='/admin/users'>
            <Button variant='secondary' className='w-full gap-2'>
              <Users size={16} />
              Manage Users
            </Button>
          </Link>
          <Button variant='secondary' className='w-full gap-2'>
            <BarChart3 size={16} />
            Export Report
          </Button>
        </div>
      </Card>
    </div>
  )
}

const KPICard = ({ icon: Icon, label, value }) => (
  <Card className='p-6'>
    <div className='flex items-center justify-between'>
      <div>
        <p className='text-sm text-gray-500'>{label}</p>
        <p className='text-2xl font-semibold text-gray-900 mt-1'>{value}</p>
      </div>
      <div className='w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center'>
        <Icon size={20} className='text-gray-600' />
      </div>
    </div>
  </Card>
)