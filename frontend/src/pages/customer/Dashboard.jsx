import React, { useState, useEffect } from 'react'
import { Card, Alert, Spinner, Button, Badge, Modal } from '../../components/UI'
import { Link, useNavigate } from 'react-router-dom'
import { apiService } from '../../services/apiService'
import { useAuthStore, useCartStore } from '../../store/store'
import {
  ShoppingBag, Heart, Package, User as UserIcon,
  TrendingUp, Clock, CheckCircle, ChevronRight,
  Star, Image as ImageIcon, Sparkles, Zap, ShieldCheck
} from 'lucide-react'
import toast from 'react-hot-toast'
import { AuthModal } from '../../components/AuthModal'

export const CustomerDashboard = () => {
  const [products, setProducts] = useState([])
  const [orders, setOrders] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const { items: cartItems } = useCartStore()
  const cartTotal = useCartStore((state) => state.getTotal())
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [productsRes, ordersRes, categoriesRes] = await Promise.all([
          apiService.getProducts(),
          user ? apiService.getOrders() : Promise.resolve({ data: { success: false, orders: [] } }),
          apiService.getCategories()
        ])

        if (productsRes.data.success) {
          setProducts(productsRes.data.products.slice(0, 6))
        }
        if (user && ordersRes.data.success) {
          setOrders(ordersRes.data.orders.slice(0, 3))
        }
        if (categoriesRes.data.success) {
          setCategories(categoriesRes.data.categories.slice(0, 5))
        }
      } catch (err) {
        setError('Failed to load dashboard data')
        toast.error('Failed to load dashboard data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [user])

  if (loading) return <Spinner />

  return (
    <div className='space-y-6'>
      {/* Hero Section */}
      <div className='relative h-[280px] md:h-[320px] rounded-lg overflow-hidden bg-gradient-to-r from-gray-900 to-gray-800'>
        <div className='absolute inset-0 opacity-30'>
          <div className='absolute inset-0' style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&q=80')",
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }} />
        </div>
        <div className='relative h-full flex flex-col items-start justify-center p-6 md:p-8 max-w-xl'>
          <Badge className='bg-white/20 text-white border-white/30 mb-3'>
            Spring Collection 2026
          </Badge>
          <h1 className='text-3xl md:text-4xl font-bold text-white leading-tight mb-3'>
            Premium Styles for Modern Living
          </h1>
          <p className='text-white/80 text-base mb-6'>
            Discover exclusive electronics, fashion, and accessories curated just for you.
          </p>
          <Link to='/customer/shop'>
            <Button variant='primary' className='bg-white text-gray-900 hover:bg-gray-100'>
              Shop New Arrivals
            </Button>
          </Link>
        </div>
      </div>

      {error && <Alert type='error' message={error} />}

      {/* Categories Section */}
      {categories.length > 0 && (
        <div>
          <div className='flex items-center justify-between mb-4'>
            <h2 className='text-lg font-semibold text-gray-900'>Shop by Category</h2>
            <Link to='/customer/shop' className='text-sm text-blue-600 hover:text-blue-700'>
              View All →
            </Link>
          </div>
          <div className='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3'>
            {categories.map(cat => (
              <Link
                key={cat.category_id}
                to={`/customer/shop?category=${cat.name}`}
                className='group p-4 bg-white border border-gray-100 rounded-lg hover:shadow-md transition-shadow text-center'
              >
                <div className='w-12 h-12 bg-gray-100 rounded-full overflow-hidden flex items-center justify-center mx-auto mb-2 group-hover:bg-gray-200 transition-colors'>
                  {cat.image ? (
                    <img src={cat.image} alt={cat.name} className='w-full h-full object-cover' />
                  ) : (
                    <Zap size={20} className='text-gray-600' />
                  )}
                </div>
                <span className='text-sm font-medium text-gray-700 block truncate'>{cat.name}</span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Main Content Grid */}
      <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
        {/* Featured Products */}
        <div className='lg:col-span-2'>
          <div className='flex items-center justify-between mb-4'>
            <h2 className='text-lg font-semibold text-gray-900'>Featured Products</h2>
            <Link to='/customer/shop' className='text-sm text-blue-600 hover:text-blue-700'>
              View All →
            </Link>
          </div>
          <div className='grid grid-cols-1 sm:grid-cols-2 gap-4'>
            {products.map((product) => (
              <ProductCard
                key={product.product_id}
                product={product}
                onAuthRequired={() => setIsAuthModalOpen(true)}
              />
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className='space-y-6'>
          {/* User Stats */}
          {user && (
            <Card className='p-6 bg-gray-50 border-gray-100'>
              <h3 className='text-sm font-medium text-gray-500 mb-4'>Your Summary</h3>
              <div className='space-y-3'>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>Active Orders</span>
                  <span className='text-lg font-semibold text-gray-900'>{orders.length}</span>
                </div>
                <div className='flex justify-between items-center'>
                  <span className='text-sm text-gray-600'>Cart Items</span>
                  <span className='text-lg font-semibold text-gray-900'>{cartItems.length}</span>
                </div>
                <div className='flex justify-between items-center pt-2 border-t border-gray-200'>
                  <span className='text-sm font-medium text-gray-900'>Cart Total</span>
                  <span className='text-xl font-bold text-gray-900'>${cartTotal.toFixed(2)}</span>
                </div>
              </div>
              <Link to='/customer/cart'>
                <Button variant='primary' className='w-full mt-4'>
                  Proceed to Checkout
                </Button>
              </Link>
            </Card>
          )}

          {/* Recent Orders */}
          {orders.length > 0 && (
            <div>
              <div className='flex items-center justify-between mb-4'>
                <h2 className='text-lg font-semibold text-gray-900'>Recent Orders</h2>
                <Link to='/customer/orders' className='text-sm text-blue-600 hover:text-blue-700'>
                  View All →
                </Link>
              </div>
              <div className='space-y-3'>
                {orders.map((order) => (
                  <Link
                    to='/customer/orders'
                    key={order.order_id}
                    className='block p-4 bg-white border border-gray-100 rounded-lg hover:shadow-md transition-shadow'
                  >
                    <div className='flex items-center justify-between'>
                      <div>
                        <p className='font-medium text-gray-900'>Order #{order.order_id}</p>
                        <p className='text-xs text-gray-500 mt-0.5'>{order.order_date}</p>
                      </div>
                      <div className='text-right'>
                        <p className='font-semibold text-gray-900'>${order.total.toFixed(2)}</p>
                        <Badge variant={order.status === 'Completed' ? 'success' : 'warning'} size='sm'>
                          {order.status}
                        </Badge>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* Sign Up Promotion */}
          {!user && (
            <Card className='p-6 bg-blue-600 border-0'>
              <h3 className='text-lg font-semibold text-white mb-2'>Join Our Community</h3>
              <p className='text-blue-100 text-sm mb-4'>Sign up to get 10% off your first order and exclusive deals.</p>
              <Button onClick={() => setIsAuthModalOpen(true)} className='w-full bg-white text-blue-600 hover:bg-gray-100'>
                Sign Up Now
              </Button>
            </Card>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <Card className='p-6'>
        <h3 className='text-lg font-semibold text-gray-900 mb-4'>Quick Actions</h3>
        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3'>
          <Link to='/customer/shop'>
            <Button variant='primary' className='w-full gap-2'>
              <ShoppingBag size={16} />
              Shop Now
            </Button>
          </Link>
          <Link to='/customer/cart'>
            <Button variant='secondary' className='w-full gap-2'>
              My Cart ({cartItems.length})
            </Button>
          </Link>
          <Link to='/customer/orders'>
            <Button variant='secondary' className='w-full gap-2'>
              <Package size={16} />
              My Orders
            </Button>
          </Link>
          <Link to='/customer/profile'>
            <Button variant='secondary' className='w-full gap-2'>
              <UserIcon size={16} />
              Profile
            </Button>
          </Link>
        </div>
      </Card>

      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={() => {
          toast.success('Welcome! You are now signed in.')
          window.location.reload()
        }}
      />
    </div>
  )
}

const ProductCard = ({ product, onAuthRequired }) => {
  const { addItem } = useCartStore()
  const [isQuickViewOpen, setIsQuickViewOpen] = useState(false)

  const handleAddToCart = () => {
    const { user } = useAuthStore.getState()
    if (!user) {
      onAuthRequired()
      return
    }
    addItem(product, 1)
    toast.success('Added to cart')
  }

  return (
    <>
      <Card className='p-4 hover:shadow-md transition-shadow'>
        {/* Product Image */}
        <div className='relative w-full h-40 bg-gray-50 rounded-lg mb-3 overflow-hidden cursor-pointer' onClick={() => setIsQuickViewOpen(true)}>
          {product.discount > 0 && (
            <div className='absolute top-2 left-2 z-10'>
              <Badge variant='danger' size='sm'>{product.discount}% OFF</Badge>
            </div>
          )}
          <button
            onClick={(e) => {
              e.stopPropagation()
              onAuthRequired()
            }}
            className='absolute top-2 right-2 z-10 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-sm hover:bg-red-50 transition-colors'
          >
            <Heart size={14} className='text-gray-400 hover:text-red-500' />
          </button>
          {product.images?.[0] ? (
            <img
              src={product.images[0]}
              alt={product.name}
              className='w-full h-full object-cover'
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/200x200?text=No+Image'
              }}
            />
          ) : (
            <div className='w-full h-full flex items-center justify-center'>
              <ShoppingBag className='w-12 h-12 text-gray-300' />
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className='space-y-2'>
          <div className='flex items-start justify-between gap-2'>
            <h3 className='font-medium text-gray-900 line-clamp-1 flex-1'>{product.name}</h3>
            <div className='flex items-center gap-1 shrink-0'>
              <Star size={12} className='fill-yellow-400 text-yellow-400' />
              <span className='text-xs text-gray-600'>{product.average_rating?.toFixed(1) || '4.5'}</span>
            </div>
          </div>
          <p className='text-xs text-gray-500 line-clamp-2'>{product.description}</p>
          <div className='flex items-center justify-between pt-2'>
            <div>
              <span className='text-lg font-semibold text-gray-900'>
                ${product.discounted_price.toFixed(2)}
              </span>
              {product.discount > 0 && (
                <span className='ml-2 text-xs text-gray-400 line-through'>
                  ${product.price.toFixed(2)}
                </span>
              )}
            </div>
            <Button
              variant='primary'
              size='sm'
              className='rounded-full w-8 h-8 p-0'
              onClick={handleAddToCart}
              disabled={product.stock === 0}
            >
              <ShoppingBag size={14} />
            </Button>
          </div>
        </div>
      </Card>

      {/* Quick View Modal */}
      <Modal
        isOpen={isQuickViewOpen}
        onClose={() => setIsQuickViewOpen(false)}
        title={product.name}
        size='lg'
      >
        <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
          <div className='bg-gray-50 rounded-lg overflow-hidden h-64'>
            {product.images?.[0] ? (
              <img
                src={product.images[0]}
                alt={product.name}
                className='w-full h-full object-cover'
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/400x400?text=No+Image'
                }}
              />
            ) : (
              <div className='w-full h-full flex items-center justify-center'>
                <ShoppingBag className='w-16 h-16 text-gray-300' />
              </div>
            )}
          </div>
          <div className='space-y-4'>
            <div>
              {product.discount > 0 && (
                <Badge variant='danger' className='mb-2'>{product.discount}% OFF</Badge>
              )}
              <p className='text-2xl font-bold text-gray-900'>
                ${product.discounted_price.toFixed(2)}
              </p>
              {product.discount > 0 && (
                <p className='text-sm text-gray-400 line-through'>
                  ${product.price.toFixed(2)}
                </p>
              )}
            </div>
            <p className='text-gray-600 text-sm leading-relaxed'>
              {product.description}
            </p>
            <div className='flex items-center gap-2'>
              <div className='flex items-center gap-1'>
                <Star size={14} className='fill-yellow-400 text-yellow-400' />
                <span className='text-sm font-medium'>{product.average_rating?.toFixed(1) || '4.5'}</span>
              </div>
              <span className='text-xs text-gray-400'>|</span>
              <span className='text-sm text-gray-500'>Stock: {product.stock} left</span>
            </div>
            <Button
              variant='primary'
              className='w-full mt-4'
              onClick={handleAddToCart}
              disabled={product.stock === 0}
            >
              Add to Cart
            </Button>
          </div>
        </div>
      </Modal>
    </>
  )
}