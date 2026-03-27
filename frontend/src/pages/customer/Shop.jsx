import React, { useState, useEffect, useMemo, useCallback } from 'react'
import { Card, Alert, Spinner, Button, Badge, Modal } from '../../components/UI'
import { apiService } from '../../services/apiService'
import { useAuthStore, useCartStore } from '../../store/store'
import {
  ShoppingBag, Heart, Search, Filter, Plus, Minus,
  X, Star, ChevronLeft, ChevronRight, SlidersHorizontal,
  Check, Truck, RotateCcw, Shield
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { AuthModal } from '../../components/AuthModal'

export const CustomerShop = () => {
  const [products, setProducts] = useState([])
  const [filteredProducts, setFilteredProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [sortBy, setSortBy] = useState('featured')
  const [priceRange, setPriceRange] = useState({ min: 0, max: 1000 })
  const [showFilters, setShowFilters] = useState(false)
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)

  useEffect(() => {
    fetchData()
  }, [])

  useEffect(() => {
    filterAndSortProducts()
  }, [products, searchTerm, selectedCategory, sortBy, priceRange])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [productsRes, categoriesRes] = await Promise.all([
        apiService.getProducts(),
        apiService.getCategories(),
      ])

      if (productsRes.data.success) {
        setProducts(productsRes.data.products)
        const maxPrice = Math.max(...productsRes.data.products.map(p => p.price))
        setPriceRange({ min: 0, max: maxPrice })
      }
      if (categoriesRes.data.success) {
        setCategories([{ category_id: 'all', name: 'All Products' }, ...categoriesRes.data.categories])
      }
    } catch (err) {
      setError('Unable to load products. Please try again.')
      toast.error('Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  const filterAndSortProducts = () => {
    let filtered = [...products]

    if (selectedCategory !== 'all') {
      filtered = filtered.filter((p) => p.category === selectedCategory)
    }

    if (searchTerm) {
      filtered = filtered.filter((p) =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.description.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    filtered = filtered.filter(
      (p) => p.price >= priceRange.min && p.price <= priceRange.max
    )

    switch (sortBy) {
      case 'price_asc':
        filtered.sort((a, b) => a.discounted_price - b.discounted_price)
        break
      case 'price_desc':
        filtered.sort((a, b) => b.discounted_price - a.discounted_price)
        break
      case 'rating':
        filtered.sort((a, b) => b.average_rating - a.average_rating)
        break
      case 'newest':
        filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        break
      default:
        filtered.sort((a, b) => b.product_id - a.product_id)
    }

    setFilteredProducts(filtered)
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
        <h1 className="text-2xl font-semibold text-gray-900 mb-1">Shop</h1>
        <p className="text-gray-500">Discover our curated collection of premium products</p>
      </div>

      {/* Search and Filter Bar */}
      <div className="bg-white rounded-lg border border-gray-100 p-4">
        <div className="flex flex-col lg:flex-row gap-3">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div className="w-full lg:w-48">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white"
            >
              {categories.map((cat) => (
                <option key={cat.category_id} value={cat.name === 'All Products' ? 'all' : cat.name}>
                  {cat.name}
                </option>
              ))}
            </select>
          </div>

          <div className="w-full lg:w-48">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500 bg-white"
            >
              <option value="featured">Featured</option>
              <option value="newest">Newest First</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="rating">Best Rating</option>
            </select>
          </div>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className="px-3 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
          >
            <SlidersHorizontal size={16} />
            <span className="text-sm">Filters</span>
          </button>
        </div>

        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price Range
                </label>
                <div className="flex items-center gap-3">
                  <input
                    type="number"
                    value={priceRange.min}
                    onChange={(e) => setPriceRange({ ...priceRange, min: Number(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                    placeholder="Min"
                  />
                  <span className="text-gray-400">—</span>
                  <input
                    type="number"
                    value={priceRange.max}
                    onChange={(e) => setPriceRange({ ...priceRange, max: Number(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                    placeholder="Max"
                  />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {error && <Alert type="error" message={error} />}

      {/* Results Count */}
      <div className="flex justify-between items-center">
        <p className="text-sm text-gray-500">
          Showing <span className="font-medium text-gray-900">{filteredProducts.length}</span> products
        </p>
      </div>

      {/* Products Grid */}
      {filteredProducts.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredProducts.map((product) => (
            <ProductCard
              key={product.product_id}
              product={product}
              onAuthRequired={() => setIsAuthModalOpen(true)}
            />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-100 text-center py-12">
          <ShoppingBag className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No products found</h3>
          <p className="text-gray-500">Try adjusting your filters or search term</p>
          <button
            onClick={() => {
              setSearchTerm('')
              setSelectedCategory('all')
              setSortBy('featured')
              setPriceRange({ min: 0, max: priceRange.max })
            }}
            className="mt-4 text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            Clear all filters
          </button>
        </div>
      )}

      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={() => toast.success('Welcome! You are now signed in.')}
      />
    </div>
  )
}

const ProductCard = ({ product, onAuthRequired }) => {
  const [showModal, setShowModal] = useState(false)
  const [quantity, setQuantity] = useState(1)
  const [selectedColor, setSelectedColor] = useState(null)
  const [selectedSize, setSelectedSize] = useState(null)
  const [currentImageIndex, setCurrentImageIndex] = useState(0)
  const [isHovered, setIsHovered] = useState(false)
  const { addItem } = useCartStore()
  const { user } = useAuthStore()

  const discountPercentage = product.discount > 0
    ? Math.round(((product.price - product.discounted_price) / product.price) * 100)
    : 0

  const handleAddToCart = useCallback(() => {
    if (!user) {
      onAuthRequired()
      return
    }

    if (quantity > product.stock) {
      toast.error('Insufficient stock')
      return
    }

    if (product.category === 'Clothes') {
      if (!selectedColor) {
        toast.error('Please select a color')
        return
      }
      if (!selectedSize) {
        toast.error('Please select a size')
        return
      }
    }

    addItem(product, quantity, selectedColor, selectedSize)
    toast.success('Added to cart')
    setShowModal(false)
    setQuantity(1)
  }, [product, quantity, selectedColor, selectedSize, addItem, user, onAuthRequired])

  const handleAddToWishlist = useCallback(async () => {
    if (!user) {
      onAuthRequired()
      return
    }
    try {
      await apiService.addToWishlist(user.user_id, product.product_id)
      toast.success('Added to wishlist')
    } catch (err) {
      toast.error('Unable to add to wishlist')
    }
  }, [user, product.product_id, onAuthRequired])

  return (
    <>
      <div
        className="group relative bg-white rounded-lg border border-gray-100 hover:shadow-md transition-all duration-200"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Image Container */}
        <div
          className="relative aspect-square bg-gray-50 cursor-pointer overflow-hidden rounded-t-lg"
          onClick={() => setShowModal(true)}
        >
          {product.images?.[currentImageIndex] ? (
            <img
              src={product.images[currentImageIndex]}
              alt={product.name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              onError={(e) => {
                e.target.src = 'https://placehold.co/400x400?text=No+Image'
              }}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <ShoppingBag className="w-12 h-12 text-gray-300" />
            </div>
          )}

          {discountPercentage > 0 && (
            <div className="absolute top-2 left-2 bg-red-500 text-white text-xs font-medium px-2 py-0.5 rounded">
              {discountPercentage}% OFF
            </div>
          )}

          {product.images?.length > 1 && isHovered && (
            <>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  setCurrentImageIndex((prev) => (prev - 1 + product.images.length) % product.images.length)
                }}
                className="absolute left-2 top-1/2 -translate-y-1/2 p-1 bg-white rounded-full shadow-sm opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <ChevronLeft size={14} />
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  setCurrentImageIndex((prev) => (prev + 1) % product.images.length)
                }}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-1 bg-white rounded-full shadow-sm opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <ChevronRight size={14} />
              </button>
            </>
          )}

          {product.stock === 0 && (
            <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
              <span className="bg-white text-gray-900 px-2 py-1 rounded text-xs font-medium">
                Out of Stock
              </span>
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="p-3">
          <h3 className="font-medium text-gray-900 mb-0.5 line-clamp-1 text-sm">
            {product.name}
          </h3>
          <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">
            {product.category}
          </p>

          <div className="flex items-center gap-1 mb-2">
            <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
            <span className="text-xs font-medium text-gray-700">
              {product.average_rating?.toFixed(1) || '4.5'}
            </span>
          </div>

          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-base font-semibold text-gray-900">
              ${product.discounted_price.toFixed(2)}
            </span>
            {product.discount > 0 && (
              <span className="text-xs text-gray-400 line-through">
                ${product.price.toFixed(2)}
              </span>
            )}
          </div>

          {product.colors?.length > 0 && (
            <div className="flex gap-1 mb-3">
              {product.colors.slice(0, 3).map((color, i) => (
                <div
                  key={i}
                  className="w-2.5 h-2.5 rounded-full border border-gray-200"
                  style={{ backgroundColor: color.toLowerCase().replace(/\s/g, '') }}
                  title={color}
                />
              ))}
              {product.colors.length > 3 && (
                <span className="text-[9px] text-gray-400">
                  +{product.colors.length - 3}
                </span>
              )}
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => setShowModal(true)}
              disabled={product.stock === 0}
              className={`flex-1 px-2 py-1.5 text-xs font-medium rounded transition-colors ${product.stock === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-900 text-white hover:bg-gray-800'
                }`}
            >
              Quick View
            </button>
            <button
              onClick={handleAddToWishlist}
              className="p-1.5 border border-gray-200 rounded hover:border-gray-300 transition-colors"
            >
              <Heart size={14} className="text-gray-600" />
            </button>
          </div>
        </div>
      </div>

      {/* Product Modal */}
      <Modal
        isOpen={showModal}
        onClose={() => {
          setShowModal(false)
          setQuantity(1)
          setCurrentImageIndex(0)
        }}
        className="max-w-4xl"
      >
        <div className="flex flex-col md:flex-row gap-6">
          {/* Image Gallery */}
          <div className="md:w-1/2">
            <div className="aspect-square bg-gray-50 rounded-lg overflow-hidden mb-3">
              {product.images?.[currentImageIndex] ? (
                <img
                  src={product.images[currentImageIndex]}
                  alt={product.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'https://placehold.co/600x600?text=No+Image'
                  }}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <ShoppingBag className="w-16 h-16 text-gray-300" />
                </div>
              )}
            </div>

            {product.images?.length > 1 && (
              <div className="grid grid-cols-5 gap-2">
                {product.images.map((img, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrentImageIndex(i)}
                    className={`aspect-square rounded-lg overflow-hidden border-2 transition-all ${i === currentImageIndex ? 'border-gray-900' : 'border-transparent opacity-60 hover:opacity-100'
                      }`}
                  >
                    <img src={img} alt="" className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Details */}
          <div className="md:w-1/2">
            <div className="mb-4">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {product.category}
                </span>
                {product.stock > 0 && product.stock < 10 && (
                  <span className="text-xs text-orange-600 bg-orange-50 px-2 py-0.5 rounded">
                    Only {product.stock} left
                  </span>
                )}
              </div>

              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                {product.name}
              </h2>

              <div className="flex items-center gap-2 mb-3">
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm font-medium">{product.average_rating?.toFixed(1) || '4.5'}</span>
                </div>
                <span className="text-gray-300">|</span>
                <span className="text-xs text-gray-500">
                  {product.review_count || 0} reviews
                </span>
              </div>

              <div className="flex items-baseline gap-2 mb-4">
                <span className="text-2xl font-bold text-gray-900">
                  ${product.discounted_price.toFixed(2)}
                </span>
                {product.discount > 0 && (
                  <>
                    <span className="text-sm text-gray-400 line-through">
                      ${product.price.toFixed(2)}
                    </span>
                    <span className="text-xs text-green-600 font-medium">
                      Save ${(product.price - product.discounted_price).toFixed(2)}
                    </span>
                  </>
                )}
              </div>

              <p className="text-gray-600 text-sm leading-relaxed">
                {product.description}
              </p>
            </div>

            {/* Color Selection */}
            {product.colors?.length > 0 && (
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Color
                </label>
                <div className="flex flex-wrap gap-2">
                  {product.colors.map((color) => (
                    <button
                      key={color}
                      onClick={() => setSelectedColor(color)}
                      className={`relative w-8 h-8 rounded-full border-2 transition-all ${selectedColor === color
                        ? 'border-gray-900 scale-110'
                        : 'border-gray-200 hover:border-gray-300'
                        }`}
                    >
                      <div
                        className="w-full h-full rounded-full"
                        style={{ backgroundColor: color.toLowerCase().replace(/\s/g, '') }}
                      />
                      {selectedColor === color && (
                        <Check className="absolute -top-1 -right-1 w-3 h-3 text-green-500 bg-white rounded-full" />
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Size Selection */}
            {product.sizes?.length > 0 && (
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Size
                </label>
                <div className="flex flex-wrap gap-2">
                  {product.sizes.map((size) => (
                    <button
                      key={size}
                      onClick={() => setSelectedSize(size)}
                      className={`min-w-[48px] h-10 px-3 rounded-lg text-sm font-medium transition-all border ${selectedSize === size
                        ? 'bg-gray-900 text-white border-gray-900'
                        : 'bg-white text-gray-700 border-gray-200 hover:border-gray-300'
                        }`}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Quantity */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quantity
              </label>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded hover:bg-gray-50 transition-colors"
                >
                  <Minus size={14} />
                </button>
                <span className="w-10 text-center font-medium">{quantity}</span>
                <button
                  onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                  className="w-8 h-8 flex items-center justify-center border border-gray-200 rounded hover:bg-gray-50 transition-colors"
                >
                  <Plus size={14} />
                </button>
              </div>
            </div>

            {/* Add to Cart Button */}
            <button
              onClick={handleAddToCart}
              disabled={product.stock === 0}
              className={`w-full py-2.5 rounded-lg font-medium transition-colors mb-4 ${product.stock === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-900 text-white hover:bg-gray-800'
                }`}
            >
              {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
            </button>

            {/* Shipping Info */}
            <div className="space-y-1.5 pt-3 border-t border-gray-100">
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <Truck size={14} />
                <span>Free shipping on orders over $50</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <RotateCcw size={14} />
                <span>30-day return policy</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <Shield size={14} />
                <span>Secure checkout</span>
              </div>
            </div>
          </div>
        </div>
      </Modal>
    </>
  )
}