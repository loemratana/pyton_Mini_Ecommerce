import React, { useState, useEffect } from 'react'
import { Card, Alert, Spinner, Button, Badge } from '../../components/UI'
import { apiService } from '../../services/apiService'
import { useAuthStore, useCartStore } from '../../store/store'
import { Heart, ShoppingBag, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

export const WishlistPage = () => {
  const [wishlistProducts, setWishlistProducts] = useState([])
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { user } = useAuthStore()
  const { addItem } = useCartStore()

  useEffect(() => {
    fetchWishlistProducts()
  }, [])

  const fetchWishlistProducts = async () => {
    try {
      setLoading(true)
      const response = await apiService.getProducts()
      if (response.data.success) {
        setProducts(response.data.products)
        const wishlist = response.data.products.filter((p) =>
          user?.wishlist?.includes(p.product_id)
        )
        setWishlistProducts(wishlist)
      }
    } catch (err) {
      setError('Failed to load wishlist')
      toast.error('Failed to load wishlist')
    } finally {
      setLoading(false)
    }
  }

  const handleRemoveFromWishlist = async (productId) => {
    try {
      await apiService.removeFromWishlist(user.user_id, productId)
      setWishlistProducts((prev) => prev.filter((p) => p.product_id !== productId))
      toast.success('Removed from wishlist')
    } catch (err) {
      toast.error('Failed to remove from wishlist')
    }
  }

  const handleAddToCart = (product) => {
    addItem(product, 1)
    toast.success('Added to cart')
  }

  if (loading) return <Spinner />

  return (
    <div className='space-y-6'>
      <h1 className='text-3xl font-bold text-gray-900'>My Wishlist</h1>

      {error && <Alert type='error' message={error} />}

      {wishlistProducts.length === 0 ? (
        <Card className='text-center py-16'>
          <Heart className='w-16 h-16 text-gray-300 mx-auto mb-4' />
          <p className='text-gray-600 text-lg mb-6'>Your wishlist is empty</p>
          <Button variant='primary' href='/customer/shop'>
            Start Shopping
          </Button>
        </Card>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {wishlistProducts.map((product) => (
            <Card key={product.product_id} className='hover:shadow-lg flex flex-col'>
              {/* Image */}
              <div className='w-full h-48 bg-gradient-to-br from-gray-200 to-gray-300 rounded-lg mb-4 flex items-center justify-center'>
                <ShoppingBag className='w-12 h-12 text-gray-400' />
              </div>

              {/* Info */}
              <h3 className='font-bold text-gray-900 mb-2 flex-1'>{product.name}</h3>
              <p className='text-sm text-gray-600 mb-3 line-clamp-2'>{product.description}</p>

              {/* Price */}
              <div className='flex items-center gap-3 mb-4'>
                <span className='text-lg font-bold text-gray-900'>
                  ${product.discounted_price.toFixed(2)}
                </span>
                {product.discount > 0 && (
                  <Badge variant='danger'>{product.discount}%</Badge>
                )}
              </div>

              {/* Stock */}
              <p className={`text-sm font-medium mb-4 ${product.stock > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
              </p>

              {/* Actions */}
              <div className='flex gap-2'>
                <Button
                  variant='primary'
                  className='flex-1'
                  onClick={() => handleAddToCart(product)}
                  disabled={product.stock === 0}
                >
                  <ShoppingBag size={18} /> Add to Cart
                </Button>
                <Button
                  variant='danger'
                  size='sm'
                  onClick={() => handleRemoveFromWishlist(product.product_id)}
                >
                  <Trash2 size={18} />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
