import React, { useState, useEffect, useRef } from 'react'
import { Card, Alert, Spinner, Button, Modal, Badge } from '../../components/UI'
import { apiService } from '../../services/apiService'
import {
  Plus, Edit2, Trash2, Search, ChevronUp, ChevronDown,
  Package, DollarSign, Percent, Layers, FileText,
  Palette, Maximize, Image as ImageIcon, X, Upload,
  Tag, AlertCircle, CheckCircle, Clock, Grid3x3,
  ChevronLeft, ChevronRight, FileSpreadsheet, Download
} from 'lucide-react'
import toast from 'react-hot-toast'
import * as XLSX from 'xlsx'

const ImageUploader = ({ values, onChange }) => {
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await apiService.uploadImage(formData)
      if (response.data.success) {
        onChange([...values, response.data.url])
        toast.success('Image uploaded')
      }
    } catch (err) {
      toast.error('Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className='space-y-3'>
      <label className='block text-sm font-medium text-gray-700 mb-2'>
        Product Images
      </label>

      <div className='grid grid-cols-4 gap-3'>
        {values.map((url, index) => (
          <div key={index} className='relative group aspect-square rounded-lg overflow-hidden border border-gray-200 bg-gray-50'>
            <img
              src={url}
              alt="product"
              className='w-full h-full object-cover'
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/100x100?text=Error'
              }}
            />
            <button
              type="button"
              onClick={() => onChange(values.filter((_, i) => i !== index))}
              className='absolute top-1 right-1 p-1.5 bg-red-500 text-white rounded-md opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600'
            >
              <Trash2 size={12} />
            </button>
          </div>
        ))}
        <button
          type="button"
          onClick={() => fileInputRef.current.click()}
          className='aspect-square rounded-lg border-2 border-dashed border-gray-300 flex flex-col items-center justify-center text-gray-400 hover:border-blue-400 hover:text-blue-400 transition-colors bg-gray-50'
        >
          {uploading ? <Spinner size="sm" /> : <><Plus size={20} /><span className='text-xs mt-1'>Add</span></>}
        </button>
      </div>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className='hidden'
        accept="image/*"
      />
    </div>
  )
}

const TagInput = ({ label, icon: Icon, values, onChange, placeholder, suggestions = [], isColor = false }) => {
  const [inputValue, setInputValue] = useState('')

  const handleAdd = (val) => {
    const trimmed = val.trim()
    if (trimmed && !values.includes(trimmed)) {
      onChange([...values, trimmed])
    }
    setInputValue('')
  }

  const handleRemove = (val) => {
    onChange(values.filter(v => v !== val))
  }

  return (
    <div className='space-y-3'>
      <label className='block text-sm font-medium text-gray-700'>
        {label}
      </label>

      {values.length > 0 && (
        <div className='flex flex-wrap gap-2'>
          {values.map(v => (
            <span
              key={v}
              className='inline-flex items-center gap-2 px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm'
            >
              {isColor && (
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: v.toLowerCase().replace(/\s/g, '') }}
                />
              )}
              {v}
              <button
                type="button"
                onClick={() => handleRemove(v)}
                className='hover:text-red-500'
              >
                <X size={14} />
              </button>
            </span>
          ))}
        </div>
      )}

      {isColor && suggestions.length > 0 && (
        <div className='flex flex-wrap gap-2'>
          {suggestions.map(s => (
            <button
              key={s}
              type="button"
              onClick={() => values.includes(s) ? handleRemove(s) : handleAdd(s)}
              className={`w-8 h-8 rounded-full border-2 transition-all ${values.includes(s) ? 'border-blue-500 scale-110' : 'border-gray-200 hover:scale-110'
                }`}
              style={{ backgroundColor: s.toLowerCase().replace(/\s/g, '') }}
              title={s}
            />
          ))}
        </div>
      )}

      <div className='flex gap-2'>
        <input
          type='text'
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault()
              handleAdd(inputValue)
            }
          }}
          className='flex-1 px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
          placeholder={placeholder}
        />
        <button
          type="button"
          onClick={() => handleAdd(inputValue)}
          className='px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors text-sm'
        >
          Add
        </button>
      </div>

      {!isColor && suggestions.length > 0 && (
        <div className='flex flex-wrap gap-2'>
          {suggestions.filter(s => !values.includes(s)).map(s => (
            <button
              key={s}
              type="button"
              onClick={() => handleAdd(s)}
              className='px-2 py-1 text-xs text-gray-600 bg-gray-100 rounded hover:bg-gray-200 transition-colors'
            >
              + {s}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export const AdminProducts = () => {
  const [products, setProducts] = useState([])
  const [filteredProducts, setFilteredProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('name')
  const [sortOrder, setSortOrder] = useState('asc')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)

  // Pagination states
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(10)

  const [formData, setFormData] = useState({
    name: '',
    price: '',
    stock: '',
    category: '',
    description: '',
    discount: '',
    colors: [],
    sizes: [],
    images: [],
  })

  useEffect(() => {
    fetchProducts()
  }, [])

  useEffect(() => {
    filterAndSortProducts()
  }, [products, searchTerm, sortBy, sortOrder])

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const response = await apiService.getProducts()
      if (response.data.success) {
        setProducts(response.data.products)
      }
    } catch (err) {
      setError('Failed to load products')
      toast.error('Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  const filterAndSortProducts = () => {
    let filtered = products.filter(
      (p) =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.category.toLowerCase().includes(searchTerm.toLowerCase())
    )

    filtered.sort((a, b) => {
      let aVal = a[sortBy]
      let bVal = b[sortBy]

      if (typeof aVal === 'string') {
        aVal = aVal.toLowerCase()
        bVal = bVal.toLowerCase()
      }

      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1
      } else {
        return aVal < bVal ? 1 : -1
      }
    })

    setFilteredProducts(filtered)
    setCurrentPage(1)
  }

  const handleOpenModal = (product = null) => {
    if (product) {
      setEditingProduct(product)
      setFormData({
        name: product.name,
        price: product.price,
        stock: product.stock,
        category: product.category,
        description: product.description,
        discount: product.discount || 0,
        colors: product.colors || [],
        sizes: product.sizes || [],
        images: product.images || [],
      })
    } else {
      setEditingProduct(null)
      setFormData({
        name: '',
        price: '',
        stock: '',
        category: '',
        description: '',
        discount: '',
        colors: [],
        sizes: [],
        images: [],
      })
    }
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingProduct(null)
  }

  const handleSaveProduct = async () => {
    try {
      const payload = {
        ...formData,
        price: parseFloat(formData.price),
        stock: parseInt(formData.stock),
        discount: parseFloat(formData.discount) || 0,
        colors: formData.colors,
        sizes: formData.sizes,
        images: formData.images,
      }

      if (editingProduct) {
        await apiService.updateProduct(editingProduct.product_id, payload)
        toast.success('Product updated successfully')
      } else {
        await apiService.createProduct(payload)
        toast.success('Product created successfully')
      }
      handleCloseModal()
      fetchProducts()
    } catch (err) {
      toast.error('Failed to save product')
    }
  }

  const handleDeleteProduct = async (productId) => {
    if (confirm('Are you sure you want to delete this product?')) {
      try {
        await apiService.deleteProduct(productId)
        toast.success('Product deleted')
        fetchProducts()
      } catch (err) {
        toast.error('Failed to delete product')
      }
    }
  }

  const exportToExcel = () => {
    try {
      const exportData = filteredProducts.map(product => ({
        'ID': product.product_id,
        'Name': product.name,
        'Category': product.category,
        'Price': product.price,
        'Discounted': product.discounted_price,
        'Discount %': product.discount || 0,
        'Stock': product.stock,
        'Colors': product.colors?.join(', ') || '-',
        'Sizes': product.sizes?.join(', ') || '-',
        'Rating': product.average_rating?.toFixed(1) || '-'
      }))

      const ws = XLSX.utils.json_to_sheet(exportData)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Products')

      const filename = `products_${new Date().toISOString().split('T')[0]}.xlsx`
      XLSX.writeFile(wb, filename)

      toast.success(`Exported ${exportData.length} products`)
    } catch (err) {
      toast.error('Failed to export')
    }
  }

  const getStockBadge = (stock) => {
    if (stock === 0) return <Badge variant='danger'>Out of Stock</Badge>
    if (stock < 10) return <Badge variant='warning'>Low Stock</Badge>
    return <Badge variant='success'>In Stock</Badge>
  }

  // Pagination
  const totalPages = Math.ceil(filteredProducts.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const paginatedProducts = filteredProducts.slice(startIndex, startIndex + itemsPerPage)

  if (loading) return <Spinner />

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex items-center justify-between flex-wrap gap-4'>
        <div>
          <h1 className='text-2xl font-semibold text-gray-900'>Products</h1>
          <p className='text-gray-500 mt-1'>Manage your product inventory</p>
        </div>
        <div className='flex gap-2'>
          <Button variant='secondary' onClick={exportToExcel} className='gap-2'>
            <FileSpreadsheet size={16} />
            Export
          </Button>
          <Button variant='primary' onClick={() => handleOpenModal()}>
            <Plus size={18} className='mr-2' />
            Add Product
          </Button>
        </div>
      </div>

      {error && <Alert type='error' message={error} />}

      {/* Filters */}
      <div className='flex flex-col sm:flex-row gap-3'>
        <div className='flex-1 relative'>
          <Search className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
          <input
            type='text'
            placeholder='Search products...'
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className='w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
          />
        </div>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className='px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white'
        >
          <option value='name'>Sort by Name</option>
          <option value='price'>Sort by Price</option>
          <option value='stock'>Sort by Stock</option>
        </select>
        <button
          onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
          className='px-3 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2'
        >
          {sortOrder === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
        </button>
        <select
          value={itemsPerPage}
          onChange={(e) => setItemsPerPage(Number(e.target.value))}
          className='px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white'
        >
          <option value={10}>10 per page</option>
          <option value={20}>20 per page</option>
          <option value={50}>50 per page</option>
        </select>
      </div>

      {/* Products Table */}
      {filteredProducts.length === 0 ? (
        <div className='bg-white rounded-lg border border-gray-100 text-center py-16'>
          <Package className='w-16 h-16 text-gray-300 mx-auto mb-4' />
          <h3 className='text-lg font-medium text-gray-900 mb-2'>No products found</h3>
          <p className='text-gray-500 mb-6'>
            {searchTerm ? 'Try adjusting your search' : 'Add your first product to get started'}
          </p>
          {!searchTerm && (
            <Button variant='primary' onClick={() => handleOpenModal()}>
              <Plus size={18} className='mr-2' />
              Add Product
            </Button>
          )}
        </div>
      ) : (
        <>
          <div className='bg-white rounded-lg border border-gray-100 overflow-hidden'>
            <div className='overflow-x-auto'>
              <table className='w-full'>
                <thead className='bg-gray-50 border-b border-gray-200'>
                  <tr>
                    <th className='px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase'>Product</th>
                    <th className='px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase'>Category</th>
                    <th className='px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase'>Price</th>
                    <th className='px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase'>Stock</th>
                    <th className='px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase'>Discount</th>
                    <th className='px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase'>Actions</th>
                  </tr>
                </thead>
                <tbody className='divide-y divide-gray-100'>
                  {paginatedProducts.map((product) => (
                    <tr key={product.product_id} className='hover:bg-gray-50 transition-colors'>
                      <td className='px-4 py-3'>
                        <div className='flex items-center gap-3'>
                          <div className='w-10 h-10 rounded-lg overflow-hidden bg-gray-100 flex-shrink-0'>
                            {product.images?.[0] ? (
                              <img
                                src={product.images[0]}
                                alt={product.name}
                                className='w-full h-full object-cover'
                              />
                            ) : (
                              <div className='w-full h-full flex items-center justify-center'>
                                <Package size={16} className='text-gray-400' />
                              </div>
                            )}
                          </div>
                          <div>
                            <p className='font-medium text-gray-900'>{product.name}</p>
                            {product.colors?.length > 0 && (
                              <div className='flex gap-1 mt-0.5'>
                                {product.colors.slice(0, 3).map((color, i) => (
                                  <div
                                    key={i}
                                    className='w-2 h-2 rounded-full border border-gray-200'
                                    style={{ backgroundColor: color.toLowerCase().replace(/\s/g, '') }}
                                  />
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className='px-4 py-3'>
                        <span className='text-sm text-gray-600'>{product.category}</span>
                      </td>
                      <td className='px-4 py-3 text-right'>
                        <span className='font-medium text-gray-900'>${product.price.toFixed(2)}</span>
                      </td>
                      <td className='px-4 py-3 text-right'>
                        {getStockBadge(product.stock)}
                      </td>
                      <td className='px-4 py-3 text-right'>
                        {product.discount > 0 ? (
                          <span className='text-sm text-red-600 font-medium'>{product.discount}% OFF</span>
                        ) : (
                          <span className='text-sm text-gray-400'>—</span>
                        )}
                      </td>
                      <td className='px-4 py-3 text-center'>
                        <div className='flex items-center justify-center gap-1'>
                          <button
                            onClick={() => handleOpenModal(product)}
                            className='p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors'
                            title='Edit'
                          >
                            <Edit2 size={16} />
                          </button>
                          <button
                            onClick={() => handleDeleteProduct(product.product_id)}
                            className='p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors'
                            title='Delete'
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className='px-4 py-3 border-t border-gray-100 flex items-center justify-between'>
                <p className='text-sm text-gray-500'>
                  Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, filteredProducts.length)} of {filteredProducts.length}
                </p>
                <div className='flex items-center gap-1'>
                  <button
                    onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                    disabled={currentPage === 1}
                    className={`p-1.5 rounded border transition-colors ${currentPage === 1
                      ? 'border-gray-200 text-gray-300 cursor-not-allowed'
                      : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                      }`}
                  >
                    <ChevronLeft size={14} />
                  </button>
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum
                    if (totalPages <= 5) pageNum = i + 1
                    else if (currentPage <= 3) pageNum = i + 1
                    else if (currentPage >= totalPages - 2) pageNum = totalPages - 4 + i
                    else pageNum = currentPage - 2 + i

                    return (
                      <button
                        key={pageNum}
                        onClick={() => setCurrentPage(pageNum)}
                        className={`w-7 h-7 text-sm rounded transition-colors ${currentPage === pageNum
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-600 hover:bg-gray-100'
                          }`}
                      >
                        {pageNum}
                      </button>
                    )
                  })}
                  <button
                    onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                    disabled={currentPage === totalPages}
                    className={`p-1.5 rounded border transition-colors ${currentPage === totalPages
                      ? 'border-gray-200 text-gray-300 cursor-not-allowed'
                      : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                      }`}
                  >
                    <ChevronRight size={14} />
                  </button>
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {/* Modal */}
      <Modal
        isOpen={isModalOpen}
        title={editingProduct ? 'Edit Product' : 'Add New Product'}
        onClose={handleCloseModal}
        size='2xl'
        actions={[
          <Button key='cancel' variant='secondary' onClick={handleCloseModal}>
            Cancel
          </Button>,
          <Button key='save' variant='primary' onClick={handleSaveProduct}>
            {editingProduct ? 'Update Product' : 'Create Product'}
          </Button>,
        ]}
      >
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/* Left Column */}
          <div className='space-y-4'>
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Product Name</label>
              <input
                type='text'
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
                placeholder='Enter product name'
              />
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Category</label>
              <input
                type='text'
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
                placeholder='e.g., Electronics, Clothing'
              />
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 resize-none'
                rows='4'
                placeholder='Product description...'
              />
            </div>
          </div>

          {/* Right Column */}
          <div className='space-y-4'>
            <div className='grid grid-cols-2 gap-4'>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-1'>Price</label>
                <div className='relative'>
                  <span className='absolute left-3 top-1/2 -translate-y-1/2 text-gray-400'>$</span>
                  <input
                    type='number'
                    step='0.01'
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                    className='w-full pl-7 pr-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
                    placeholder='0.00'
                  />
                </div>
              </div>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-1'>Discount (%)</label>
                <input
                  type='number'
                  step='1'
                  value={formData.discount}
                  onChange={(e) => setFormData({ ...formData, discount: e.target.value })}
                  className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
                  placeholder='0'
                />
              </div>
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-700 mb-1'>Stock Quantity</label>
              <input
                type='number'
                value={formData.stock}
                onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
                placeholder='Available quantity'
              />
            </div>

            <TagInput
              label="Colors"
              icon={Palette}
              values={formData.colors}
              onChange={(newVal) => setFormData({ ...formData, colors: newVal })}
              placeholder="Type a color..."
              suggestions={['Black', 'White', 'Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Pink']}
              isColor={true}
            />

            <TagInput
              label="Sizes"
              icon={Maximize}
              values={formData.sizes}
              onChange={(newVal) => setFormData({ ...formData, sizes: newVal })}
              placeholder="Type a size..."
              suggestions={['XS', 'S', 'M', 'L', 'XL', 'XXL']}
            />

            <ImageUploader
              values={formData.images}
              onChange={(newImages) => setFormData({ ...formData, images: newImages })}
            />
          </div>
        </div>
      </Modal>
    </div>
  )
}