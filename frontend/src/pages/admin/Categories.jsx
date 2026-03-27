import React, { useState, useEffect, useRef } from 'react'
import { Card, Alert, Spinner, Button, Modal, Badge } from '../../components/UI'
import { apiService } from '../../services/apiService'
import { Plus, Edit2, Trash2, Search, Layers, FileText, ChevronUp, ChevronDown, Tag, Upload, Image as ImageIcon } from 'lucide-react'
import toast from 'react-hot-toast'

export const AdminCategories = () => {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingCategory, setEditingCategory] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    image: '',
  })
  const fileInputRef = useRef(null)
  const [uploadingImage, setUploadingImage] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    try {
      setLoading(true)
      const response = await apiService.getCategories()
      if (response.data.success) {
        setCategories(response.data.categories)
      }
    } catch (err) {
      setError('Failed to load categories')
      toast.error('Failed to load categories')
    } finally {
      setLoading(false)
    }
  }

  const handleOpenModal = (category = null) => {
    if (category) {
      setEditingCategory(category)
      setFormData({
        name: category.name,
        description: category.description || '',
        image: category.image || '',
      })
    } else {
      setEditingCategory(null)
      setFormData({ name: '', description: '', image: '' })
    }
    setIsModalOpen(true)
  }

  const handleImageUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploadingImage(true)
    const formDataObj = new FormData()
    formDataObj.append('file', file)

    try {
      const response = await apiService.uploadImage(formDataObj)
      if (response.data.success) {
        setFormData(prev => ({ ...prev, image: response.data.url }))
        toast.success('Category image uploaded')
      }
    } catch (err) {
      toast.error('Upload failed')
    } finally {
      setUploadingImage(false)
    }
  }

  const handleSaveCategory = async (e) => {
    e.preventDefault()
    if (!formData.name.trim()) {
      toast.error('Category name is required')
      return
    }

    try {
      setIsSaving(true)
      let response
      if (editingCategory) {
        response = await apiService.updateCategory(editingCategory.category_id, formData)
      } else {
        response = await apiService.createCategory(formData)
      }

      if (response.data.success) {
        toast.success(editingCategory ? 'Category updated' : 'Category created')
        setIsModalOpen(false)
        fetchCategories()
      }
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to save category')
    } finally {
      setIsSaving(false)
    }
  }

  const handleDeleteCategory = async (id) => {
    if (!window.confirm('Are you sure you want to delete this category? Products in this category will remain but their category link will be broken.')) return

    try {
      const response = await apiService.deleteCategory(id)
      if (response.data.success) {
        toast.success('Category deleted')
        fetchCategories()
      }
    } catch (err) {
      toast.error('Failed to delete category')
    }
  }

  const filteredCategories = categories.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.description.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) return <Spinner />

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex items-center justify-between flex-wrap gap-4'>
        <div>
          <h1 className='text-3xl font-bold text-gray-900'>Categories</h1>
          <p className='text-gray-600 mt-1'>Manage your product categories</p>
        </div>
        <Button variant='primary' onClick={() => handleOpenModal()}>
          <Plus size={20} className='mr-2' />
          Add Category
        </Button>
      </div>

      {error && <Alert type='error' message={error} />}

      {/* Search Bar */}
      <div className='relative'>
        <Search className='absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400' />
        <input
          type='text'
          placeholder='Search categories...'
          className='w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Stats */}
      <div className='flex justify-end'>
        <Badge variant='primary' className='text-sm'>
          Total: {categories.length} categories
        </Badge>
      </div>

      {/* Categories Grid */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
        {filteredCategories.length > 0 ? (
          filteredCategories.map((category) => (
            <Card key={category.category_id} className='p-6 hover:shadow-lg transition-shadow'>
              <div className='flex justify-between items-start mb-4'>
                <div className='w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center overflow-hidden border border-blue-100'>
                  {category.image ? (
                    <img src={category.image} alt={category.name} className='w-full h-full object-cover' />
                  ) : (
                    <Layers size={24} className='text-blue-600' />
                  )}
                </div>
                <div className='flex gap-1'>
                  <button
                    onClick={() => handleOpenModal(category)}
                    className='p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition'
                    title='Edit'
                  >
                    <Edit2 size={18} />
                  </button>
                  <button
                    onClick={() => handleDeleteCategory(category.category_id)}
                    className='p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition'
                    title='Delete'
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>

              <h3 className='text-lg font-semibold text-gray-900 mb-2'>{category.name}</h3>
              <p className='text-gray-500 text-sm line-clamp-2 mb-4'>
                {category.description || 'No description provided'}
              </p>

              <div className='pt-4 border-t border-gray-100 flex items-center justify-between'>
                <span className='text-xs text-gray-400'>ID: {category.category_id}</span>
                <Badge variant='secondary' size='sm'>
                  {category.product_count || 0} products
                </Badge>
              </div>
            </Card>
          ))
        ) : (
          <Card className='col-span-full text-center py-12'>
            <Layers className='w-16 h-16 text-gray-300 mx-auto mb-4' />
            <p className='text-gray-500 text-lg'>No categories found</p>
            {searchTerm && (
              <p className='text-gray-400 text-sm mt-2'>Try adjusting your search term</p>
            )}
          </Card>
        )}
      </div>

      {/* Add/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        title={editingCategory ? 'Edit Category' : 'Add New Category'}
        onClose={() => setIsModalOpen(false)}
        size='lg'
        actions={[
          <Button key='cancel' variant='secondary' onClick={() => setIsModalOpen(false)}>
            Cancel
          </Button>,
          <Button
            key='save'
            variant='primary'
            onClick={handleSaveCategory}
            disabled={isSaving}
          >
            {isSaving ? <Spinner size='sm' /> : (editingCategory ? 'Update Category' : 'Create Category')}
          </Button>,
        ]}
      >
        <form onSubmit={handleSaveCategory} className='space-y-6'>
          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Category Name
            </label>
            <input
              type='text'
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500'
              placeholder='Enter category name'
              required
            />
          </div>

          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className='w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 resize-none'
              placeholder='Describe what this category is for...'
              rows='4'
            />
          </div>

          <div>
            <label className='block text-sm font-medium text-gray-700 mb-2'>
              Category Image
            </label>
            <div className='flex items-center gap-4'>
              <div 
                className='w-20 h-20 bg-gray-50 border border-gray-200 rounded-lg overflow-hidden flex items-center justify-center flex-shrink-0 cursor-pointer hover:bg-gray-100 transition-colors'
                onClick={() => fileInputRef.current?.click()}
              >
                {formData.image ? (
                  <img src={formData.image} alt="Preview" className='w-full h-full object-cover' />
                ) : (
                  <ImageIcon size={24} className='text-gray-400' />
                )}
              </div>
              <div className='flex-1'>
                <Button 
                  type='button' 
                  variant='secondary' 
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploadingImage}
                >
                  {uploadingImage ? <Spinner size="sm" /> : <><Upload size={16} className='mr-2' /> Upload Image</>}
                </Button>
                <p className='text-xs text-gray-500 mt-2'>Recommend using an image at least 400x400px</p>
              </div>
            </div>
            {formData.image && (
              <button 
                type="button" 
                onClick={() => setFormData(prev => ({ ...prev, image: '' }))}
                className='text-xs text-red-500 hover:text-red-600 mt-2'
              >
                Remove image
              </button>
            )}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleImageUpload}
              className='hidden'
              accept="image/*"
            />
          </div>
        </form>
      </Modal>
    </div>
  )
}