import React, { useState, useEffect } from 'react'
import { Card, Alert, Spinner, Badge, Button, Modal } from '../../components/UI'
import { apiService } from '../../services/apiService'
import {
  Package, Eye, ChevronRight, Calendar, CreditCard, MapPin, Clock,
  Download, FileText, Search, Filter, RefreshCw, Star, MessageCircle,
  Truck, CheckCircle, XCircle, AlertCircle, DollarSign, ShoppingBag,
  Printer, Share2, HelpCircle, ThumbsUp, Smile, Award
} from 'lucide-react'
import toast from 'react-hot-toast'
import { Invoice } from '../../components/Invoice'
import { useAuthStore } from '../../store/store'

export const CustomerOrders = () => {
  const [orders, setOrders] = useState([])
  const [filteredOrders, setFilteredOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [showInvoice, setShowInvoice] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [dateFilter, setDateFilter] = useState('all')
  const [showReviewModal, setShowReviewModal] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [reviewData, setReviewData] = useState({ rating: 5, comment: '' })
  const [submittingReview, setSubmittingReview] = useState(false)
  const [trackingModal, setTrackingModal] = useState(false)
  const [trackingInfo, setTrackingInfo] = useState(null)
  const { user } = useAuthStore()

  useEffect(() => {
    fetchOrders()
  }, [])

  useEffect(() => {
    filterOrders()
  }, [orders, searchTerm, statusFilter, dateFilter])

  const fetchOrders = async () => {
    try {
      setLoading(true)
      const response = await apiService.getOrders()
      if (response.data.success) {
        setOrders(response.data.orders)
      }
    } catch (err) {
      setError('Unable to load your orders. Please try again.')
      toast.error('Failed to load orders')
    } finally {
      setLoading(false)
    }
  }

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm('Are you sure you want to cancel this order? This action cannot be undone.')) return
    try {
      const res = await apiService.cancelOrder(orderId)
      if (res.data.success) {
        toast.success('Order cancelled successfully')
        setIsModalOpen(false)
        fetchOrders()
      }
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to cancel order')
    }
  }

  const filterOrders = () => {
    let filtered = [...orders]

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(order =>
        order.order_id.toString().includes(searchTerm) ||
        order.items.some(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(order => order.status === statusFilter)
    }

    // Date filter
    const now = new Date()
    if (dateFilter === 'week') {
      const weekAgo = new Date(now.setDate(now.getDate() - 7))
      filtered = filtered.filter(order => new Date(order.order_date) >= weekAgo)
    } else if (dateFilter === 'month') {
      const monthAgo = new Date(now.setMonth(now.getMonth() - 1))
      filtered = filtered.filter(order => new Date(order.order_date) >= monthAgo)
    } else if (dateFilter === 'year') {
      const yearAgo = new Date(now.setFullYear(now.getFullYear() - 1))
      filtered = filtered.filter(order => new Date(order.order_date) >= yearAgo)
    }

    setFilteredOrders(filtered)
  }

  const handleSubmitReview = async () => {
    if (!reviewData.comment.trim()) {
      toast.error('Please write a review')
      return
    }
    setSubmittingReview(true)
    try {
      await apiService.submitReview({
        product_id: selectedProduct.product_id,
        order_id: selectedOrder?.order_id,
        rating: reviewData.rating,
        comment: reviewData.comment
      })
      toast.success('Review submitted successfully!')
      setShowReviewModal(false)
      setReviewData({ rating: 5, comment: '' })
    } catch (err) {
      toast.error('Failed to submit review')
    } finally {
      setSubmittingReview(false)
    }
  }

  const handleTrackOrder = async (order) => {
    setTrackingInfo(null)
    setTrackingModal(true)
    try {
      const response = await apiService.trackOrder(order.order_id)
      if (response.data.success) {
        setTrackingInfo(response.data.tracking)
      }
    } catch (err) {
      toast.error('Tracking information unavailable')
    }
  }

  const handleReorder = async (order) => {
    try {
      for (const item of order.items) {
        await apiService.addToCart({
          product_id: item.product_id,
          quantity: item.quantity,
          color: item.color,
          size: item.size
        })
      }
      toast.success('Items added to cart!')
    } catch (err) {
      toast.error('Failed to reorder')
    }
  }

  const getStatusConfig = (status) => {
    const configs = {
      'Pending': {
        color: 'warning',
        icon: Clock,
        text: 'Processing',
        bgColor: 'bg-yellow-50',
        textColor: 'text-yellow-700',
        borderColor: 'border-yellow-200',
        progress: 25
      },
      'Processing': {
        color: 'info',
        icon: Clock,
        text: 'Processing',
        bgColor: 'bg-blue-50',
        textColor: 'text-blue-700',
        borderColor: 'border-blue-200',
        progress: 50
      },
      'Shipped': {
        color: 'primary',
        icon: Truck,
        text: 'Shipped',
        bgColor: 'bg-purple-50',
        textColor: 'text-purple-700',
        borderColor: 'border-purple-200',
        progress: 75
      },
      'Delivered': {
        color: 'success',
        icon: CheckCircle,
        text: 'Delivered',
        bgColor: 'bg-green-50',
        textColor: 'text-green-700',
        borderColor: 'border-green-200',
        progress: 100
      },
      'Completed': {
        color: 'success',
        icon: CheckCircle,
        text: 'Completed',
        bgColor: 'bg-green-50',
        textColor: 'text-green-700',
        borderColor: 'border-green-200',
        progress: 100
      },
      'Cancelled': {
        color: 'danger',
        icon: XCircle,
        text: 'Cancelled',
        bgColor: 'bg-red-50',
        textColor: 'text-red-700',
        borderColor: 'border-red-200',
        progress: 0
      }
    }
    return configs[status] || configs['Pending']
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const formatRelativeTime = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
    return formatDate(dateString)
  }

  const stats = {
    total: orders.length,
    delivered: orders.filter(o => o.status === 'Delivered' || o.status === 'Completed').length,
    processing: orders.filter(o => o.status === 'Processing' || o.status === 'Pending').length,
    totalSpent: orders.reduce((sum, o) => sum + o.total, 0)
  }

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <Spinner />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with Stats */}
      <div className="bg-white border border-gray-100 rounded-lg p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900 mb-1">My Orders</h1>
            <p className="text-gray-500">Track and manage your purchases</p>
          </div>
          <div className="flex gap-2">
            <Button variant="secondary" size="sm" onClick={fetchOrders} className="gap-2">
              <RefreshCw size={14} />
              Refresh
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-gray-100">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            <p className="text-xs text-gray-500">Total Orders</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">{stats.delivered}</p>
            <p className="text-xs text-gray-500">Delivered</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">{stats.processing}</p>
            <p className="text-xs text-gray-500">Processing</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-purple-600">${stats.totalSpent.toFixed(0)}</p>
            <p className="text-xs text-gray-500">Total Spent</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white border border-gray-100 rounded-lg p-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search by order ID or product..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white"
          >
            <option value="all">All Status</option>
            <option value="Pending">Pending</option>
            <option value="Processing">Processing</option>
            <option value="Shipped">Shipped</option>
            <option value="Delivered">Delivered</option>
            <option value="Cancelled">Cancelled</option>
          </select>
          <select
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white"
          >
            <option value="all">All Time</option>
            <option value="week">Last 7 Days</option>
            <option value="month">Last 30 Days</option>
            <option value="year">Last Year</option>
          </select>
        </div>
      </div>

      {error && <Alert type="error" message={error} />}

      {/* Orders List */}
      {filteredOrders.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-100 text-center py-16">
          <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No orders found</h3>
          <p className="text-gray-500 mb-6">
            {searchTerm || statusFilter !== 'all' ? 'Try adjusting your filters' : 'When you place an order, it will appear here'}
          </p>
          {(searchTerm || statusFilter !== 'all') ? (
            <Button variant="secondary" onClick={() => {
              setSearchTerm('')
              setStatusFilter('all')
              setDateFilter('all')
            }}>
              Clear Filters
            </Button>
          ) : (
            <Button variant="primary" onClick={() => window.location.href = '/customer/shop'}>
              Start Shopping
            </Button>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {filteredOrders.map((order) => {
            const statusConfig = getStatusConfig(order.status)
            const StatusIcon = statusConfig.icon

            return (
              <div
                key={order.order_id}
                className="bg-white rounded-lg border border-gray-100 hover:shadow-md transition-shadow"
              >
                <div className="p-6">
                  {/* Order Header */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="text-sm font-medium text-gray-500">Order #{order.order_id}</span>
                        <div className={`px-2 py-1 rounded-full ${statusConfig.bgColor} ${statusConfig.textColor} text-xs font-medium flex items-center gap-1`}>
                          <StatusIcon size={12} />
                          <span>{statusConfig.text}</span>
                        </div>
                        <span className="text-xs text-gray-400 flex items-center gap-1">
                          <Calendar size={12} />
                          {formatRelativeTime(order.order_date)}
                        </span>
                      </div>
                      <div className="flex items-center gap-3 text-xs text-gray-500">
                        <span>{order.items.length} {order.items.length === 1 ? 'item' : 'items'}</span>
                        <span>•</span>
                        <span>${order.total.toFixed(2)} total</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleTrackOrder(order)}
                        className="gap-1"
                      >
                        <Truck size={14} />
                        Track
                      </Button>
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => {
                          setSelectedOrder(order)
                          setIsModalOpen(true)
                        }}
                        className="gap-1"
                      >
                        <Eye size={14} />
                        Details
                      </Button>
                    </div>
                  </div>

                  {/* Progress Bar for Active Orders */}
                  {order.status !== 'Delivered' && order.status !== 'Completed' && order.status !== 'Cancelled' && (
                    <div className="mb-4">
                      <div className="flex justify-between text-xs text-gray-500 mb-1">
                        <span>Order Status</span>
                        <span>{statusConfig.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-100 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${statusConfig.progress}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {/* Order Items Preview */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {order.items.slice(0, 3).map((item, idx) => (
                      <div key={idx} className="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                        {item.image ? (
                          <img
                            src={item.image}
                            alt={item.name}
                            className="w-10 h-10 rounded-lg object-cover"
                            onError={(e) => e.target.style.display = 'none'}
                          />
                        ) : (
                          <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                            <Package size={16} className="text-gray-400" />
                          </div>
                        )}
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">{item.name}</p>
                          <p className="text-xs text-gray-500">
                            Qty: {item.quantity}
                            {item.color && ` • ${item.color}`}
                            {item.size && ` • ${item.size}`}
                          </p>
                        </div>
                        <p className="text-sm font-medium text-gray-900">
                          ${(item.price * item.quantity).toFixed(2)}
                        </p>
                      </div>
                    ))}
                  </div>
                  {order.items.length > 3 && (
                    <p className="text-xs text-gray-400 mt-3 text-center">
                      +{order.items.length - 3} more items
                    </p>
                  )}

                  {/* Action Buttons for Delivered Orders */}
                  {order.status === 'Delivered' && (
                    <div className="mt-4 pt-4 border-t border-gray-100 flex justify-end gap-2">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleReorder(order)}
                        className="gap-1"
                      >
                        <ShoppingBag size={14} />
                        Reorder
                      </Button>
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => {
                          setSelectedOrder(order)
                          setShowInvoice(true)
                        }}
                        className="gap-1"
                      >
                        <FileText size={14} />
                        Invoice
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Order Details Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        className="max-w-4xl"
      >
        {selectedOrder && (
          <div className="divide-y divide-gray-100">
            {/* Modal Header */}
            <div className="pb-6">
              <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
                <div>
                  <h2 className="text-2xl font-semibold text-gray-900">
                    Order #{selectedOrder.order_id}
                  </h2>
                  <p className="text-sm text-gray-500 mt-1">
                    Placed on {formatDate(selectedOrder.order_date)}
                  </p>
                </div>
                <div className="flex gap-2">
                  <div className={`px-3 py-1.5 rounded-full ${getStatusConfig(selectedOrder.status).bgColor} ${getStatusConfig(selectedOrder.status).textColor} text-sm font-medium flex items-center gap-2`}>
                    {React.createElement(getStatusConfig(selectedOrder.status).icon, { size: 16 })}
                    <span>{getStatusConfig(selectedOrder.status).text}</span>
                  </div>
                  <button
                    onClick={() => {
                      setIsModalOpen(false)
                      setShowInvoice(true)
                    }}
                    className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                    title="View Invoice"
                  >
                    <Printer size={18} />
                  </button>
                </div>
              </div>
            </div>

            {/* Order Timeline */}
            <div className="py-6">
              <OrderTimeline status={selectedOrder.status} />
            </div>

            {/* Order Information */}
            <div className="py-6">
              <h3 className="text-sm font-medium text-gray-900 mb-4">Order Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {selectedOrder.shipping_address && (
                  <div className="flex gap-3">
                    <MapPin size={18} className="text-gray-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-1">Shipping Address</p>
                      <p className="text-sm text-gray-600">{selectedOrder.shipping_address}</p>
                    </div>
                  </div>
                )}
                {selectedOrder.payment_method && (
                  <div className="flex gap-3">
                    <CreditCard size={18} className="text-gray-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-1">Payment Method</p>
                      <p className="text-sm text-gray-600 capitalize">{selectedOrder.payment_method}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Order Items */}
            <div className="py-6">
              <h3 className="text-sm font-medium text-gray-900 mb-4">Order Items</h3>
              <div className="space-y-3">
                {selectedOrder.items.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-4 py-3 border-b border-gray-100 last:border-0">
                    {item.image ? (
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-14 h-14 rounded-lg object-cover bg-gray-50"
                        onError={(e) => e.target.style.display = 'none'}
                      />
                    ) : (
                      <div className="w-14 h-14 bg-gray-50 rounded-lg flex items-center justify-center">
                        <Package size={20} className="text-gray-400" />
                      </div>
                    )}
                    <div className="flex-1">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-medium text-gray-900">{item.name}</p>
                          <div className="flex flex-wrap gap-2 mt-1">
                            <span className="text-xs text-gray-500">Qty: {item.quantity}</span>
                            {item.color && (
                              <span className="text-xs text-gray-500 flex items-center gap-1">
                                <span className="inline-block w-2 h-2 rounded-full" style={{
                                  backgroundColor: item.color.toLowerCase().replace(/\s/g, '')
                                }} />
                                {item.color}
                              </span>
                            )}
                            {item.size && (
                              <span className="text-xs text-gray-500">Size: {item.size}</span>
                            )}
                          </div>
                        </div>
                        <p className="font-medium text-gray-900">
                          ${(item.price * item.quantity).toFixed(2)}
                        </p>
                      </div>
                    </div>
                    {selectedOrder.status === 'Delivered' && (
                      <button
                        onClick={() => {
                          setSelectedProduct(item)
                          setShowReviewModal(true)
                        }}
                        className="px-3 py-1.5 text-xs font-medium text-blue-600 border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors"
                      >
                        <Star size={12} className="inline mr-1" />
                        Review
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Order Summary */}
            <div className="pt-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Subtotal</span>
                    <span className="text-gray-900">${(selectedOrder.subtotal || selectedOrder.total).toFixed(2)}</span>
                  </div>
                  {selectedOrder.shipping > 0 && (
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Shipping</span>
                      <span className="text-gray-900">${selectedOrder.shipping.toFixed(2)}</span>
                    </div>
                  )}
                  {selectedOrder.tax > 0 && (
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Tax</span>
                      <span className="text-gray-900">${selectedOrder.tax.toFixed(2)}</span>
                    </div>
                  )}
                  {selectedOrder.discount > 0 && (
                    <div className="flex justify-between text-sm text-green-600">
                      <span>Discount</span>
                      <span>-${selectedOrder.discount.toFixed(2)}</span>
                    </div>
                  )}
                  <div className="border-t border-gray-200 pt-2 mt-2">
                    <div className="flex justify-between">
                      <span className="text-base font-semibold text-gray-900">Total</span>
                      <span className="text-xl font-bold text-gray-900">${selectedOrder.total.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-6 flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
                Close
              </Button>
              {selectedOrder.status !== 'Cancelled' && selectedOrder.status !== 'Delivered' && selectedOrder.status !== 'Completed' && (
                <Button variant="danger" className="gap-2" onClick={() => handleCancelOrder(selectedOrder.order_id)}>
                  <XCircle size={16} />
                  Cancel Order
                </Button>
              )}
              {selectedOrder.status === 'Delivered' && (
                <Button variant="primary" className="gap-2" onClick={() => handleReorder(selectedOrder)}>
                  <ShoppingBag size={16} />
                  Buy Again
                </Button>
              )}
            </div>
          </div>
        )}
      </Modal>

      {/* Tracking Modal */}
      <Modal
        isOpen={trackingModal}
        onClose={() => setTrackingModal(false)}
        title="Track Your Order"
        size="md"
      >
        {trackingInfo ? (
          <div className="space-y-4">
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <Truck className="w-12 h-12 text-blue-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-gray-900">Your order is on the way!</p>
              <p className="text-xs text-gray-500 mt-1">Estimated delivery: {trackingInfo.estimated_delivery}</p>
            </div>
            <div className="space-y-3">
              {trackingInfo.updates?.map((update, idx) => (
                <div key={idx} className="flex gap-3">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mt-2" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{update.status}</p>
                    <p className="text-xs text-gray-500">{update.date} - {update.location}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <AlertCircle className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">Tracking information will be available once your order ships.</p>
          </div>
        )}
      </Modal>

      {/* Review Modal */}
      <Modal
        isOpen={showReviewModal}
        onClose={() => setShowReviewModal(false)}
        title="Write a Review"
        size="md"
        actions={[
          <Button key="cancel" variant="secondary" onClick={() => setShowReviewModal(false)}>
            Cancel
          </Button>,
          <Button key="submit" variant="primary" onClick={handleSubmitReview} disabled={submittingReview}>
            {submittingReview ? <Spinner size="sm" /> : 'Submit Review'}
          </Button>
        ]}
      >
        <div className="space-y-4">
          {selectedProduct && (
            <>
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                {selectedProduct.image ? (
                  <img src={selectedProduct.image} alt={selectedProduct.name} className="w-12 h-12 rounded-lg object-cover" />
                ) : (
                  <Package className="w-12 h-12 text-gray-300" />
                )}
                <div>
                  <p className="font-medium text-gray-900">{selectedProduct.name}</p>
                  <p className="text-xs text-gray-500">Rate your experience</p>
                </div>
              </div>

              <div className="flex justify-center gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => setReviewData({ ...reviewData, rating: star })}
                    className={`p-1 transition-transform ${reviewData.rating >= star ? 'scale-110' : ''}`}
                  >
                    <Star
                      size={28}
                      className={reviewData.rating >= star ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}
                    />
                  </button>
                ))}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Your Review</label>
                <textarea
                  value={reviewData.comment}
                  onChange={(e) => setReviewData({ ...reviewData, comment: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
                  rows="4"
                  placeholder="Share your experience with this product..."
                />
              </div>
            </>
          )}
        </div>
      </Modal>

      {/* Invoice Modal */}
      <Modal
        isOpen={showInvoice}
        onClose={() => setShowInvoice(false)}
        title="Order Invoice"
        size="4xl"
      >
        {selectedOrder && <Invoice order={selectedOrder} user={user} />}
      </Modal>
    </div>
  )
}


const OrderTimeline = ({ status }) => {
  const steps = [
    { label: 'Confirmed', icon: CheckCircle, desc: 'Order received', activeStatus: ['Pending', 'Processing', 'Shipped', 'Delivered', 'Completed'] },
    { label: 'Processed', icon: Clock, desc: 'Preparing order', activeStatus: ['Processing', 'Shipped', 'Delivered', 'Completed'] },
    { label: 'Shipped', icon: Truck, desc: 'Out for delivery', activeStatus: ['Shipped', 'Delivered', 'Completed'] },
    { label: 'Delivered', icon: CheckCircle, desc: 'Received', activeStatus: ['Delivered', 'Completed'] }
  ]

  const getStepStatus = (stepActiveStatus) => {
    if (status === 'Cancelled') return 'cancelled'
    if (stepActiveStatus.includes(status)) return 'completed'
    if (status === 'Pending' && stepActiveStatus.includes('Pending')) return 'current'
    return 'pending'
  }

  return (
    <div className='relative'>
      <div className='flex justify-between items-start'>
        {steps.map((step, idx) => {
          const stepStatus = getStepStatus(step.activeStatus)
          const Icon = step.icon

          return (
            <div key={idx} className='flex-1 text-center'>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-2 ${stepStatus === 'completed' ? 'bg-green-600 text-white' :
                stepStatus === 'current' ? 'bg-blue-600 text-white' :
                  stepStatus === 'cancelled' ? 'bg-red-100 text-red-500' :
                    'bg-gray-100 text-gray-400'
                }`}>
                <Icon size={18} />
              </div>
              <p className={`text-xs font-medium ${stepStatus === 'completed' || stepStatus === 'current' ? 'text-gray-900' : 'text-gray-400'
                }`}>
                {step.label}
              </p>
              <p className='text-[10px] text-gray-400 mt-1 hidden sm:block'>{step.desc}</p>
            </div>
          )
        })}
      </div>
    </div>
  )
}