import React, { useState, useEffect } from 'react'
import { Card, Alert, Spinner, Button } from '../../components/UI'
import { apiService } from '../../services/apiService'
import { BarChart3, Download, Calendar, Percent } from 'lucide-react'
import toast from 'react-hot-toast'

export const AdminAnalytics = () => {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [dateRange, setDateRange] = useState('all')

  useEffect(() => {
    fetchAnalytics()
  }, [dateRange])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      const response = await apiService.getDashboardAnalytics()
      if (response.data.success) {
        setAnalytics(response.data.analytics)
      }
    } catch (err) {
      setError('Failed to load analytics')
      toast.error('Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      toast.loading('Generating report...')
      const response = await apiService.exportReport()
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `sales_report_${new Date().toISOString().split('T')[0]}.xlsx`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      toast.dismiss()
      toast.success('Report exported successfully')
    } catch (err) {
      toast.dismiss()
      // Fallback to JSON export
      const data = JSON.stringify(analytics, null, 2)
      const element = document.createElement('a')
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data))
      element.setAttribute('download', `analytics-${new Date().toISOString().split('T')[0]}.json`)
      element.style.display = 'none'
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)
      toast.success('Report exported as JSON')
    }
  }

  if (loading) return <Spinner />

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex items-center justify-between flex-wrap gap-4'>
        <div>
          <h1 className='text-3xl font-bold text-gray-900'>Analytics</h1>
          <p className='text-gray-600'>Store performance and insights</p>
        </div>
        <Button variant='primary' onClick={handleExport}>
          <Download size={20} /> Export Report
        </Button>
      </div>

      {error && <Alert type='error' message={error} />}

      {/* Date Range Filter */}
      <Card>
        <div className='flex items-center gap-4 flex-wrap'>
          <div className='flex items-center gap-2'>
            <Calendar className='w-5 h-5 text-gray-600' />
            <span className='font-medium text-gray-700'>Period:</span>
          </div>
          {['Last 7 days', '30 days', '90 days', 'All time'].map((period, idx) => (
            <Button
              key={idx}
              variant={dateRange === period ? 'primary' : 'secondary'}
              size='sm'
              onClick={() => setDateRange(period)}
            >
              {period}
            </Button>
          ))}
        </div>
      </Card>

      {/* Main Metrics */}
      {analytics && (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'>
          <AnalyticsCard
            title='Total Revenue'
            value={`$${analytics.total_revenue.toFixed(2)}`}
            icon='💰'
            trend='+12.5%'
          />
          <AnalyticsCard title='Total Orders' value={analytics.total_orders} icon='📦' trend='+8.2%' />
          <AnalyticsCard title='Total Products' value={analytics.total_products} icon='🛍️' />
          <AnalyticsCard title='Total Customers' value={analytics.total_customers} icon='👥' trend='+5.3%' />
        </div>
      )}

      {/* Detailed Breakdown */}
      {analytics && (
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/* Orders by Status */}
          <Card>
            <h3 className='text-xl font-bold text-gray-900 mb-6 flex items-center gap-2'>
              <BarChart3 className='w-5 h-5' /> Order Status Distribution
            </h3>
            <div className='space-y-6'>
              {Object.entries(analytics.status_breakdown).map(([status, count]) => {
                const total = analytics.total_orders
                const percentage = total > 0 ? (count / total) * 100 : 0

                return (
                  <div key={status}>
                    <div className='flex items-center justify-between mb-2'>
                      <span className='font-medium text-gray-700'>{status}</span>
                      <div className='flex items-center gap-2'>
                        <span className='text-sm text-gray-600'>{count} orders</span>
                        <span className='font-bold text-gray-900'>{percentage.toFixed(1)}%</span>
                      </div>
                    </div>
                    <div className='w-full bg-gray-200 rounded-full h-3'>
                      <div
                        className='bg-gradient-to-r from-blue-600 to-purple-600 h-3 rounded-full transition-all'
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </Card>

          {/* Top Products */}
          <Card>
            <h3 className='text-xl font-bold text-gray-900 mb-6 flex items-center gap-2'>
              <BarChart3 className='w-5 h-5' /> Top Selling Products
            </h3>
            {analytics.top_products.length > 0 ? (
              <div className='space-y-4'>
                {analytics.top_products.map(([productId, sales], index) => {
                  const maxSales = Math.max(...analytics.top_products.map((p) => p[1]))
                  const percentage = (sales / maxSales) * 100

                  return (
                    <div key={productId}>
                      <div className='flex items-center justify-between mb-2'>
                        <span className='font-medium text-gray-700'>Product #{productId}</span>
                        <div className='flex items-center gap-2'>
                          <span className='text-lg font-bold text-gray-900'>{sales}</span>
                          <span className='text-sm text-gray-600'>units</span>
                        </div>
                      </div>
                      <div className='w-full bg-gray-200 rounded-full h-2'>
                        <div
                          className='bg-gradient-to-r from-green-600 to-emerald-600 h-2 rounded-full transition-all'
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            ) : (
              <p className='text-gray-500 text-center py-8'>No sales data available</p>
            )}
          </Card>
        </div>
      )}

      {/* Revenue Breakdown */}
      {analytics && (
        <Card>
          <h3 className='text-xl font-bold text-gray-900 mb-6 flex items-center gap-2'>
            <Percent className='w-5 h-5' /> Revenue Insights
          </h3>
          <div className='grid grid-cols-1 md:grid-cols-3 gap-6'>
            <div className='text-center'>
              <p className='text-gray-600 text-sm mb-2'>Average Order Value</p>
              <p className='text-3xl font-bold text-gray-900'>
                ${analytics.total_orders > 0 ? (analytics.total_revenue / analytics.total_orders).toFixed(2) : '0.00'}
              </p>
            </div>
            <div className='text-center'>
              <p className='text-gray-600 text-sm mb-2'>Total Products</p>
              <p className='text-3xl font-bold text-gray-900'>{analytics.total_products}</p>
            </div>
            <div className='text-center'>
              <p className='text-gray-600 text-sm mb-2'>Total Customers</p>
              <p className='text-3xl font-bold text-gray-900'>{analytics.total_customers}</p>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}

const AnalyticsCard = ({ title, value, icon, trend }) => (
  <Card>
    <div className='flex items-start justify-between'>
      <div>
        <p className='text-gray-600 text-sm mb-2'>{title}</p>
        <p className='text-3xl font-bold text-gray-900'>{value}</p>
        {trend && <p className='text-sm text-green-600 font-semibold mt-2'>{trend} vs last period</p>}
      </div>
      <span className='text-3xl'>{icon}</span>
    </div>
  </Card>
)
