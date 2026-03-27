import React, { useState, useEffect } from 'react'
import { Card, Alert, Spinner, Button, Badge, Modal } from '../../components/UI'
import { apiService } from '../../services/apiService'
import {
  Package, Search, Clock, CheckCircle, TrendingUp, Eye,
  ChevronUp, ChevronDown, Filter, Calendar, DollarSign,
  User, Truck, XCircle, RefreshCw, Download, Printer,
  ChevronLeft, ChevronRight, FileSpreadsheet, FileText
} from 'lucide-react'
import toast from 'react-hot-toast'
import * as XLSX from 'xlsx'

export const AdminOrders = () => {
  const [orders, setOrders] = useState([])
  const [filteredOrders, setFilteredOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [newStatus, setNewStatus] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [sortField, setSortField] = useState('order_date')
  const [sortDirection, setSortDirection] = useState('desc')
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false)

  // Pagination states
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(10)
  const [totalPages, setTotalPages] = useState(1)

  useEffect(() => {
    fetchOrders()
  }, [])

  useEffect(() => {
    filterAndSortOrders()
  }, [orders, searchTerm, statusFilter, sortField, sortDirection])

  useEffect(() => {
    setTotalPages(Math.ceil(filteredOrders.length / itemsPerPage))
    setCurrentPage(1)
  }, [filteredOrders, itemsPerPage])

  const fetchOrders = async () => {
    try {
      setLoading(true)
      const response = await apiService.getOrders()
      if (response.data.success) {
        setOrders(response.data.orders)
      }
    } catch (err) {
      setError('Failed to load orders')
      toast.error('Failed to load orders')
    } finally {
      setLoading(false)
    }
  }

  const filterAndSortOrders = () => {
    let filtered = [...orders]

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(
        (order) =>
          order.order_id.toString().includes(searchTerm) ||
          order.customer?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          order.items?.some(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(order => order.status === statusFilter)
    }

    // Sorting
    filtered.sort((a, b) => {
      let aVal, bVal
      switch (sortField) {
        case 'order_id':
          aVal = a.order_id
          bVal = b.order_id
          break
        case 'total':
          aVal = a.total
          bVal = b.total
          break
        case 'items_count':
          aVal = a.items?.length || 0
          bVal = b.items?.length || 0
          break
        default:
          aVal = new Date(a.order_date)
          bVal = new Date(b.order_date)
      }
      if (sortDirection === 'asc') {
        return aVal > bVal ? 1 : -1
      } else {
        return aVal < bVal ? 1 : -1
      }
    })

    setFilteredOrders(filtered)
  }

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const handleUpdateStatus = async () => {
    if (!newStatus) return

    try {
      await apiService.updateOrderStatus(selectedOrder.order_id, { status: newStatus })
      toast.success('Order status updated successfully')
      setIsModalOpen(false)
      fetchOrders()
    } catch (err) {
      toast.error('Failed to update order')
    }
  }

  const exportToExcel = () => {
    try {
      // Prepare data for export
      const exportData = filteredOrders.map(order => ({
        'Order ID': order.order_id,
        'Date': new Date(order.order_date).toLocaleDateString(),
        'Customer': order.customer,
        'Items': order.items?.length || 0,
        'Subtotal': order.subtotal || order.total,
        'Shipping': order.shipping || 0,
        'Tax': order.tax || 0,
        'Total': order.total,
        'Status': order.status,
        'Payment Method': order.payment_method || 'N/A',
        'Shipping Address': order.shipping_address || 'N/A'
      }))

      // Create worksheet
      const ws = XLSX.utils.json_to_sheet(exportData)

      // Set column widths
      const colWidths = [
        { wch: 10 }, // Order ID
        { wch: 12 }, // Date
        { wch: 20 }, // Customer
        { wch: 8 },  // Items
        { wch: 12 }, // Subtotal
        { wch: 10 }, // Shipping
        { wch: 8 },  // Tax
        { wch: 12 }, // Total
        { wch: 12 }, // Status
        { wch: 15 }, // Payment Method
        { wch: 30 }  // Shipping Address
      ]
      ws['!cols'] = colWidths

      // Create workbook
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Orders')

      // Generate filename with current date
      const filename = `orders_export_${new Date().toISOString().split('T')[0]}.xlsx`

      // Download file
      XLSX.writeFile(wb, filename)

      toast.success(`Exported ${exportData.length} orders to Excel`)
    } catch (err) {
      toast.error('Failed to export orders')
      console.error('Export error:', err)
    }
  }

  const exportCurrentPageToExcel = () => {
    try {
      const startIndex = (currentPage - 1) * itemsPerPage
      const endIndex = startIndex + itemsPerPage
      const currentPageData = paginatedOrders

      const exportData = currentPageData.map(order => ({
        'Order ID': order.order_id,
        'Date': new Date(order.order_date).toLocaleDateString(),
        'Customer': order.customer,
        'Items': order.items?.length || 0,
        'Subtotal': order.subtotal || order.total,
        'Shipping': order.shipping || 0,
        'Tax': order.tax || 0,
        'Total': order.total,
        'Status': order.status,
        'Payment Method': order.payment_method || 'N/A',
        'Shipping Address': order.shipping_address || 'N/A'
      }))

      const ws = XLSX.utils.json_to_sheet(exportData)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, `Orders_Page_${currentPage}`)

      const filename = `orders_page_${currentPage}_${new Date().toISOString().split('T')[0]}.xlsx`
      XLSX.writeFile(wb, filename)

      toast.success(`Exported page ${currentPage} (${exportData.length} orders) to Excel`)
    } catch (err) {
      toast.error('Failed to export current page')
    }
  }

  const getStatusConfig = (status) => {
    const configs = {
      'Pending': {
        icon: Clock,
        text: 'Pending',
        bgColor: 'bg-yellow-50',
        textColor: 'text-yellow-700',
        borderColor: 'border-yellow-200'
      },
      'Processing': {
        icon: TrendingUp,
        text: 'Processing',
        bgColor: 'bg-blue-50',
        textColor: 'text-blue-700',
        borderColor: 'border-blue-200'
      },
      'Shipped': {
        icon: Truck,
        text: 'Shipped',
        bgColor: 'bg-purple-50',
        textColor: 'text-purple-700',
        borderColor: 'border-purple-200'
      },
      'Delivered': {
        icon: CheckCircle,
        text: 'Delivered',
        bgColor: 'bg-green-50',
        textColor: 'text-green-700',
        borderColor: 'border-green-200'
      },
      'Completed': {
        icon: CheckCircle,
        text: 'Completed',
        bgColor: 'bg-green-50',
        textColor: 'text-green-700',
        borderColor: 'border-green-200'
      },
      'Cancelled': {
        icon: XCircle,
        text: 'Cancelled',
        bgColor: 'bg-red-50',
        textColor: 'text-red-700',
        borderColor: 'border-red-200'
      }
    }
    return configs[status] || configs['Pending']
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const stats = {
    total: orders.length,
    pending: orders.filter(o => o.status === 'Pending').length,
    processing: orders.filter(o => o.status === 'Processing').length,
    delivered: orders.filter(o => o.status === 'Delivered' || o.status === 'Completed').length,
    totalRevenue: orders.reduce((sum, o) => sum + o.total, 0)
  }

  // Pagination logic
  const indexOfLastItem = currentPage * itemsPerPage
  const indexOfFirstItem = indexOfLastItem - itemsPerPage
  const paginatedOrders = filteredOrders.slice(indexOfFirstItem, indexOfLastItem)

  const goToPage = (page) => {
    setCurrentPage(Math.min(Math.max(1, page), totalPages))
  }

  const goToPreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1)
    }
  }

  const goToNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1)
    }
  }

  const SortIcon = ({ field }) => {
    if (sortField !== field) return <ChevronUp size={14} className="opacity-30" />
    return sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
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
      {/* Header */}
      <div className="bg-white border border-gray-100 rounded-lg p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900 mb-1">Orders Management</h1>
            <p className="text-gray-500">Manage customer orders and track shipments</p>
          </div>
          <div className="flex gap-2">
            <Button variant="secondary" size="sm" onClick={fetchOrders} className="gap-2">
              <RefreshCw size={14} />
              Refresh
            </Button>
            <div className="relative group">
              <Button variant="secondary" size="sm" className="gap-2">
                <FileSpreadsheet size={14} />
                Export
              </Button>
              <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
                <button
                  onClick={exportToExcel}
                  className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 rounded-t-lg flex items-center gap-2"
                >
                  <FileSpreadsheet size={14} />
                  Export All ({filteredOrders.length}) Orders
                </button>
                <button
                  onClick={exportCurrentPageToExcel}
                  className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 rounded-b-lg flex items-center gap-2"
                >
                  <FileText size={14} />
                  Export Current Page ({paginatedOrders.length}) Orders
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-gray-100">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            <p className="text-xs text-gray-500">Total Orders</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
            <p className="text-xs text-gray-500">Pending</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">{stats.processing}</p>
            <p className="text-xs text-gray-500">Processing</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">{stats.delivered}</p>
            <p className="text-xs text-gray-500">Delivered</p>
          </div>
        </div>
      </div>

      {error && <Alert type="error" message={error} />}

      {/* Filters */}
      <div className="bg-white border border-gray-100 rounded-lg p-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search by Order ID, Customer or Product..."
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
            <option value="Completed">Completed</option>
            <option value="Cancelled">Cancelled</option>
          </select>
          <select
            value={itemsPerPage}
            onChange={(e) => {
              setItemsPerPage(Number(e.target.value))
              setCurrentPage(1)
            }}
            className="px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white"
          >
            <option value={5}>5 per page</option>
            <option value={10}>10 per page</option>
            <option value={20}>20 per page</option>
            <option value={50}>50 per page</option>
          </select>
        </div>
      </div>

      {/* Orders Table */}
      {filteredOrders.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-100 text-center py-16">
          <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No orders found</h3>
          <p className="text-gray-500 mb-6">
            {searchTerm || statusFilter !== 'all' ? 'Try adjusting your filters' : 'When customers place orders, they will appear here'}
          </p>
          {(searchTerm || statusFilter !== 'all') && (
            <Button variant="secondary" onClick={() => {
              setSearchTerm('')
              setStatusFilter('all')
            }}>
              Clear Filters
            </Button>
          )}
        </div>
      ) : (
        <>
          <div className="bg-white rounded-lg border border-gray-100 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700" onClick={() => handleSort('order_id')}>
                      <div className="flex items-center gap-1">
                        Order ID
                        <SortIcon field="order_id" />
                      </div>
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700" onClick={() => handleSort('order_date')}>
                      <div className="flex items-center gap-1">
                        Date
                        <SortIcon field="order_date" />
                      </div>
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Customer
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700" onClick={() => handleSort('items_count')}>
                      <div className="flex items-center gap-1">
                        Items
                        <SortIcon field="items_count" />
                      </div>
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700" onClick={() => handleSort('total')}>
                      <div className="flex items-center gap-1">
                        Total
                        <SortIcon field="total" />
                      </div>
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-4 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {paginatedOrders.map((order) => {
                    const statusConfig = getStatusConfig(order.status)
                    const StatusIcon = statusConfig.icon
                    const itemCount = order.items?.length || 0

                    return (
                      <tr key={order.order_id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4">
                          <span className="font-mono text-sm font-medium text-gray-900">
                            #{order.order_id}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <Calendar size={14} className="text-gray-400" />
                            <span className="text-sm text-gray-600">{formatDate(order.order_date)}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <User size={14} className="text-gray-400" />
                            <span className="text-sm font-medium text-gray-900">{order.customer}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-sm text-gray-600">{itemCount} {itemCount === 1 ? 'item' : 'items'}</span>
                        </td>
                        <td className="px-6 py-4">
                          <span className="text-sm font-semibold text-gray-900">
                            {formatCurrency(order.total)}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full ${statusConfig.bgColor} ${statusConfig.textColor}`}>
                            <StatusIcon size={12} />
                            <span className="text-xs font-medium">{statusConfig.text}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center justify-center gap-2">
                            <button
                              onClick={() => {
                                setSelectedOrder(order)
                                setIsDetailsModalOpen(true)
                              }}
                              className="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                              title="View Details"
                            >
                              <Eye size={16} />
                            </button>
                            <button
                              onClick={() => {
                                setSelectedOrder(order)
                                setNewStatus(order.status)
                                setIsModalOpen(true)
                              }}
                              className="p-1.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                              title="Update Status"
                            >
                              <RefreshCw size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 flex flex-col sm:flex-row items-center justify-between gap-4">
              <p className="text-sm text-gray-500">
                Showing {indexOfFirstItem + 1} to {Math.min(indexOfLastItem, filteredOrders.length)} of {filteredOrders.length} orders
              </p>
              <div className="flex items-center gap-2">
                <button
                  onClick={goToPreviousPage}
                  disabled={currentPage === 1}
                  className={`p-2 rounded-lg border border-gray-200 transition-colors ${currentPage === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                >
                  <ChevronLeft size={16} />
                </button>

                <div className="flex items-center gap-1">
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum
                    if (totalPages <= 5) {
                      pageNum = i + 1
                    } else if (currentPage <= 3) {
                      pageNum = i + 1
                    } else if (currentPage >= totalPages - 2) {
                      pageNum = totalPages - 4 + i
                    } else {
                      pageNum = currentPage - 2 + i
                    }

                    if (pageNum > 0 && pageNum <= totalPages) {
                      return (
                        <button
                          key={pageNum}
                          onClick={() => goToPage(pageNum)}
                          className={`w-8 h-8 rounded-lg text-sm font-medium transition-colors ${currentPage === pageNum
                            ? 'bg-blue-600 text-white'
                            : 'text-gray-600 hover:bg-gray-100'
                            }`}
                        >
                          {pageNum}
                        </button>
                      )
                    }
                    return null
                  })}
                </div>

                <button
                  onClick={goToNextPage}
                  disabled={currentPage === totalPages}
                  className={`p-2 rounded-lg border border-gray-200 transition-colors ${currentPage === totalPages
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                >
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Update Status Modal */}
      <Modal
        isOpen={isModalOpen}
        title="Update Order Status"
        onClose={() => setIsModalOpen(false)}
        actions={[
          <Button key="cancel" variant="secondary" onClick={() => setIsModalOpen(false)}>
            Cancel
          </Button>,
          <Button key="save" variant="primary" onClick={handleUpdateStatus}>
            Update Status
          </Button>,
        ]}
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Order #{selectedOrder?.order_id}</label>
            <p className="text-sm text-gray-500 mb-4">Current Status: <Badge variant="warning">{selectedOrder?.status}</Badge></p>
            <label className="block text-sm font-medium text-gray-700 mb-2">New Status</label>
            <select
              value={newStatus}
              onChange={(e) => setNewStatus(e.target.value)}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
            >
              <option value="">Select Status...</option>
              <option value="Pending">Pending</option>
              <option value="Processing">Processing</option>
              <option value="Shipped">Shipped</option>
              <option value="Delivered">Delivered</option>
              <option value="Completed">Completed</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>
        </div>
      </Modal>

      {/* Order Details Modal */}
      <Modal
        isOpen={isDetailsModalOpen}
        onClose={() => setIsDetailsModalOpen(false)}
        title={`Order #${selectedOrder?.order_id}`}
        className="max-w-4xl"
      >
        {selectedOrder && (
          <div className="divide-y divide-gray-100">
            {/* Order Header */}
            <div className="pb-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-sm text-gray-500">Placed on {formatDate(selectedOrder.order_date)}</p>
                  <p className="text-sm text-gray-500 mt-1">Customer: {selectedOrder.customer}</p>
                </div>
                <Badge variant={getStatusConfig(selectedOrder.status).text === 'Pending' ? 'warning' : 'success'}>
                  {selectedOrder.status}
                </Badge>
              </div>
            </div>

            {/* Order Items */}
            <div className="py-6">
              <h3 className="text-sm font-medium text-gray-900 mb-4">Order Items</h3>
              <div className="space-y-3">
                {selectedOrder.items?.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-4 py-3 border-b border-gray-100 last:border-0">
                    {item.image ? (
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-12 h-12 rounded-lg object-cover bg-gray-50"
                        onError={(e) => e.target.style.display = 'none'}
                      />
                    ) : (
                      <div className="w-12 h-12 bg-gray-50 rounded-lg flex items-center justify-center">
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
                  <div className="border-t border-gray-200 pt-2 mt-2">
                    <div className="flex justify-between">
                      <span className="text-base font-semibold text-gray-900">Total</span>
                      <span className="text-xl font-bold text-gray-900">${selectedOrder.total.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Shipping Address */}
            {selectedOrder.shipping_address && (
              <div className="pt-6">
                <h3 className="text-sm font-medium text-gray-900 mb-3">Shipping Address</h3>
                <p className="text-sm text-gray-600">{selectedOrder.shipping_address}</p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="pt-6 flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setIsDetailsModalOpen(false)}>
                Close
              </Button>
              <Button
                variant="primary"
                onClick={() => {
                  setIsDetailsModalOpen(false)
                  setSelectedOrder(selectedOrder)
                  setNewStatus(selectedOrder.status)
                  setIsModalOpen(true)
                }}
              >
                Update Status
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}