import React, { useState } from 'react'
import { Card, Alert, Button, Modal, Badge } from '../../components/UI'
import { useCartStore, useAuthStore } from '../../store/store'
import { apiService } from '../../services/apiService'
import { ShoppingCart, Trash2, Plus, Minus, ArrowRight, CreditCard, Truck, ShieldCheck, X, Tag, Percent } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { Invoice } from '../../components/Invoice'
import { CheckCircle2 } from 'lucide-react'

export const CartPage = () => {
  const { items, removeItem, updateQuantity, clearCart, getTotal } = useCartStore()
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false)
  const [checkoutData, setCheckoutData] = useState({
    payment_method: 'card',
    shipping_address: '',
    card_number: '',
    card_expiry: '',
    card_cvc: '',
    card_name: '',
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [showSuccessModal, setShowSuccessModal] = useState(false)
  const [lastOrder, setLastOrder] = useState(null)
  const [couponCode, setCouponCode] = useState('')
  const [appliedCoupon, setAppliedCoupon] = useState(null)
  const [couponLoading, setCouponLoading] = useState(false)

  const subtotal = getTotal()
  const couponDiscount = appliedCoupon ? appliedCoupon.discount_amount : 0
  const shipping = appliedCoupon?.free_shipping ? 0 : (subtotal > 50 ? 0 : 5.99)
  const tax = ((subtotal - couponDiscount) * 0.08).toFixed(2)
  const total = subtotal - couponDiscount + shipping + parseFloat(tax)

  const handleApplyCoupon = async () => {
    if (!couponCode.trim()) return
    setCouponLoading(true)
    try {
      const res = await apiService.validateCoupon({ code: couponCode, subtotal })
      if (res.data.success) {
        setAppliedCoupon(res.data.coupon)
        toast.success(`Coupon applied! ${res.data.coupon.description}`)
      }
    } catch (err) {
      toast.error(err.response?.data?.message || 'Invalid coupon code')
      setAppliedCoupon(null)
    } finally {
      setCouponLoading(false)
    }
  }

  const handleRemoveCoupon = () => {
    setAppliedCoupon(null)
    setCouponCode('')
    toast.success('Coupon removed')
  }

  const handleCheckout = async () => {
    if (!checkoutData.shipping_address.trim()) {
      toast.error('Please enter a shipping address')
      return
    }

    if (checkoutData.payment_method === 'card') {
      if (!checkoutData.card_number.replace(/\s/g, '') || checkoutData.card_number.replace(/\s/g, '').length < 16) {
        toast.error('Please enter a valid 16-digit card number')
        return
      }
      if (!checkoutData.card_expiry || !/^(0[1-9]|1[0-2])\/\d{2}$/.test(checkoutData.card_expiry)) {
        toast.error('Please enter a valid expiry date (MM/YY)')
        return
      }
      if (!checkoutData.card_cvc || checkoutData.card_cvc.length < 3) {
        toast.error('Please enter a valid CVC')
        return
      }
      if (!checkoutData.card_name.trim()) {
        toast.error('Please enter the name on card')
        return
      }
    }

    setIsProcessing(true)

    try {
      if (checkoutData.payment_method === 'card') {
        // Simulate real payment processing time
        await new Promise((resolve) => setTimeout(resolve, 1500))
      }

      const orderData = {
        items: items.map((item) => ({
          product_id: item.product_id,
          name: item.name,
          price: item.discounted_price,
          quantity: item.quantity,
          color: item.selectedColor,
          size: item.selectedSize,
          image: item.images?.[0] || ''
        })),
        subtotal: subtotal,
        shipping: shipping,
        tax: parseFloat(tax),
        total: total,
        payment_method: checkoutData.payment_method,
        shipping_address: checkoutData.shipping_address,
      }

      const response = await apiService.createOrder(orderData)
      if (response.data.success) {
        toast.success('Order placed successfully!')
        setLastOrder({
          ...orderData,
          order_id: response.data.order_id,
          order_date: new Date().toISOString()
        })
        clearCart()
        setIsCheckoutOpen(false)
        setShowSuccessModal(true)
      }
    } catch (err) {
      toast.error('Failed to process order')
    } finally {
      setIsProcessing(false)
    }
  }

  if (items.length === 0) {
    return (
      <div className='min-h-[70vh] flex items-center justify-center'>
        <div className='text-center space-y-6 max-w-md mx-auto'>
          <div className='w-32 h-32 bg-gray-50 rounded-full flex items-center justify-center mx-auto'>
            <ShoppingCart className='w-12 h-12 text-gray-300' />
          </div>
          <div>
            <h2 className='text-2xl font-semibold text-gray-900 mb-2'>Your cart is empty</h2>
            <p className='text-gray-500 mb-8'>Looks like you haven't added any items to your cart yet.</p>
            <Button variant='primary' size='lg' onClick={() => navigate('/customer/shop')} className='px-8'>
              Start Shopping
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className='max-w-7xl mx-auto px-4 py-8'>
      {/* Header */}
      <div className='mb-8'>
        <h1 className='text-3xl font-bold text-gray-900'>Shopping Cart</h1>
        <p className='text-gray-500 mt-1'>{items.length} {items.length === 1 ? 'item' : 'items'}</p>
      </div>

      <div className='grid grid-cols-1 lg:grid-cols-3 gap-8'>
        {/* Cart Items */}
        <div className='lg:col-span-2 space-y-4'>
          {items.map((item, index) => (
            <CartItem
              key={`${item.product_id}-${item.selectedColor}-${item.selectedSize}-${index}`}
              item={item}
              onRemove={removeItem}
              onUpdateQuantity={updateQuantity}
            />
          ))}

          {/* Actions */}
          <div className='flex justify-between items-center pt-4'>
            <Button
              variant='secondary'
              onClick={() => navigate('/customer/shop')}
              className='text-gray-600'
            >
              ← Continue Shopping
            </Button>
            <button
              onClick={clearCart}
              className='text-sm text-gray-400 hover:text-red-500 transition-colors'
            >
              Clear Cart
            </button>
          </div>
        </div>

        {/* Order Summary */}
        <div className='lg:col-span-1'>
          <div className='bg-white rounded-xl border border-gray-200 p-6 sticky top-24'>
            <h2 className='text-lg font-semibold text-gray-900 mb-6'>Order Summary</h2>

            {/* Coupon Code Section */}
            <div className='mb-6'>
              <label className='block text-sm font-medium text-gray-700 mb-2'>Promo Code</label>
              {appliedCoupon ? (
                <div className='flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg'>
                  <div className='flex items-center gap-2'>
                    <Tag size={16} className='text-green-600' />
                    <div>
                      <span className='text-sm font-semibold text-green-700'>{appliedCoupon.code}</span>
                      <p className='text-xs text-green-600'>{appliedCoupon.description}</p>
                    </div>
                  </div>
                  <button onClick={handleRemoveCoupon} className='text-gray-400 hover:text-red-500'>
                    <X size={16} />
                  </button>
                </div>
              ) : (
                <div className='flex gap-2'>
                  <input
                    type='text'
                    value={couponCode}
                    onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                    placeholder='Enter code'
                    className='flex-1 px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-500'
                    onKeyDown={(e) => e.key === 'Enter' && handleApplyCoupon()}
                  />
                  <Button
                    variant='secondary'
                    size='sm'
                    onClick={handleApplyCoupon}
                    disabled={couponLoading}
                  >
                    {couponLoading ? '...' : 'Apply'}
                  </Button>
                </div>
              )}
            </div>

            <div className='space-y-3 mb-6'>
              <div className='flex justify-between text-sm'>
                <span className='text-gray-600'>Subtotal</span>
                <span className='font-medium text-gray-900'>${subtotal.toFixed(2)}</span>
              </div>
              {appliedCoupon && couponDiscount > 0 && (
                <div className='flex justify-between text-sm'>
                  <span className='text-green-600 flex items-center gap-1'>
                    <Percent size={12} /> Discount ({appliedCoupon.discount_percent}%)
                  </span>
                  <span className='font-medium text-green-600'>-${couponDiscount.toFixed(2)}</span>
                </div>
              )}
              <div className='flex justify-between text-sm'>
                <span className='text-gray-600'>Shipping</span>
                {shipping === 0 ? (
                  <span className='text-green-600 font-medium'>Free</span>
                ) : (
                  <span className='font-medium text-gray-900'>${shipping.toFixed(2)}</span>
                )}
              </div>
              <div className='flex justify-between text-sm'>
                <span className='text-gray-600'>Estimated Tax</span>
                <span className='font-medium text-gray-900'>${tax}</span>
              </div>

              <div className='border-t border-gray-200 my-4' />

              <div className='flex justify-between'>
                <span className='text-base font-semibold text-gray-900'>Total</span>
                <span className='text-2xl font-bold text-gray-900'>${total.toFixed(2)}</span>
              </div>
            </div>

            <Button
              variant='primary'
              size='lg'
              className='w-full mb-4'
              onClick={() => setIsCheckoutOpen(true)}
            >
              Proceed to Checkout
              <ArrowRight size={18} className='ml-2' />
            </Button>

            {/* Trust Badges */}
            <div className='space-y-3 pt-4 border-t border-gray-100'>
              <div className='flex items-center gap-2 text-xs text-gray-500'>
                <ShieldCheck size={14} />
                <span>Secure checkout</span>
              </div>
              <div className='flex items-center gap-2 text-xs text-gray-500'>
                <Truck size={14} />
                <span>Free shipping on orders over $50</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Checkout Modal */}
      <Modal
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        className='max-w-2xl'
      >
        <div className='p-6'>
          {/* Modal Header */}
          <div className='flex justify-between items-center mb-6'>
            <h2 className='text-2xl font-semibold text-gray-900'>Complete Your Order</h2>
            <button
              onClick={() => setIsCheckoutOpen(false)}
              className='p-2 hover:bg-gray-100 rounded-lg transition-colors'
            >
              <X size={20} className='text-gray-400' />
            </button>
          </div>

          <div className='space-y-6'>
            {/* Order Items Summary */}
            <div className='bg-gray-50 rounded-lg p-4'>
              <h3 className='font-medium text-gray-900 mb-3'>Order Summary</h3>
              <div className='space-y-3 max-h-64 overflow-y-auto'>
                {items.map((item, index) => (
                  <div key={index} className='flex items-center gap-3'>
                    <div className='w-12 h-12 bg-white rounded-lg overflow-hidden flex-shrink-0 border border-gray-200'>
                      <img
                        src={item.images?.[0] || ''}
                        alt={item.name}
                        className='w-full h-full object-cover'
                        onError={(e) => e.target.src = 'https://via.placeholder.com/50'}
                      />
                    </div>
                    <div className='flex-1 min-w-0'>
                      <p className='text-sm font-medium text-gray-900 truncate'>{item.name}</p>
                      <p className='text-xs text-gray-500'>
                        {item.selectedColor && `${item.selectedColor} / `}
                        {item.selectedSize && `${item.selectedSize} / `}
                        Qty: {item.quantity}
                      </p>
                    </div>
                    <span className='text-sm font-medium text-gray-900'>
                      ${(item.discounted_price * item.quantity).toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
              <div className='border-t border-gray-200 mt-4 pt-4 flex justify-between'>
                <span className='font-medium text-gray-900'>Total</span>
                <span className='text-lg font-bold text-gray-900'>${total.toFixed(2)}</span>
              </div>
            </div>

            {/* Shipping Address */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Shipping Address
              </label>
              <textarea
                value={checkoutData.shipping_address}
                onChange={(e) =>
                  setCheckoutData({ ...checkoutData, shipping_address: e.target.value })
                }
                placeholder='Enter your full delivery address...'
                className='w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none'
                rows='3'
              />
            </div>

            {/* Payment Method */}
            <div>
              <label className='block text-sm font-medium text-gray-700 mb-2'>
                Payment Method
              </label>
              <div className='grid grid-cols-2 gap-3 mb-4'>
                {[
                  { id: 'card', name: 'Credit Card', icon: CreditCard },
                  { id: 'paypal', name: 'PayPal', icon: ShieldCheck },
                  { id: 'apple_pay', name: 'Apple Pay', icon: ShieldCheck },
                  { id: 'cash', name: 'Cash on Delivery', icon: Truck },
                ].map((method) => (
                  <button
                    key={method.id}
                    onClick={() => setCheckoutData({ ...checkoutData, payment_method: method.id })}
                    className={`flex items-center gap-3 p-3 border rounded-lg transition-all ${checkoutData.payment_method === method.id
                      ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500/20'
                      : 'border-gray-200 hover:border-gray-300'
                      }`}
                  >
                    <method.icon size={20} className={checkoutData.payment_method === method.id ? 'text-blue-600' : 'text-gray-400'} />
                    <span className={`text-sm font-medium ${checkoutData.payment_method === method.id ? 'text-blue-700' : 'text-gray-700'
                      }`}>
                      {method.name}
                    </span>
                  </button>
                ))}
              </div>

              {/* Credit Card Details Form */}
              {checkoutData.payment_method === 'card' && (
                <div className='bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-4 animate-in fade-in slide-in-from-top-2'>
                  <div>
                    <label className='block text-xs font-medium text-gray-700 mb-1'>Name on Card</label>
                    <input
                      type='text'
                      placeholder='John Doe'
                      value={checkoutData.card_name}
                      onChange={(e) => setCheckoutData({ ...checkoutData, card_name: e.target.value })}
                      className='w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm'
                    />
                  </div>
                  <div>
                    <label className='block text-xs font-medium text-gray-700 mb-1'>Card Number</label>
                    <div className='relative'>
                      <CreditCard className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400' />
                      <input
                        type='text'
                        placeholder='0000 0000 0000 0000'
                        maxLength='19'
                        value={checkoutData.card_number}
                        onChange={(e) => {
                          let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '')
                          let formattedValue = ''
                          for (let i = 0; i < value.length; i++) {
                            if (i > 0 && i % 4 === 0) formattedValue += ' '
                            formattedValue += value[i]
                          }
                          setCheckoutData({ ...checkoutData, card_number: formattedValue })
                        }}
                        className='w-full pl-9 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm font-mono'
                      />
                    </div>
                  </div>
                  <div className='grid grid-cols-2 gap-4'>
                    <div>
                      <label className='block text-xs font-medium text-gray-700 mb-1'>Expiry Date</label>
                      <input
                        type='text'
                        placeholder='MM/YY'
                        maxLength='5'
                        value={checkoutData.card_expiry}
                        onChange={(e) => {
                          let value = e.target.value.replace(/[^0-9]/gi, '')
                          if (value.length >= 2) value = value.substring(0, 2) + '/' + value.substring(2, 4)
                          setCheckoutData({ ...checkoutData, card_expiry: value })
                        }}
                        className='w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm font-mono'
                      />
                    </div>
                    <div>
                      <label className='block text-xs font-medium text-gray-700 mb-1'>CVC/CVV</label>
                      <input
                        type='text'
                        placeholder='123'
                        maxLength='4'
                        value={checkoutData.card_cvc}
                        onChange={(e) => setCheckoutData({ ...checkoutData, card_cvc: e.target.value.replace(/[^0-9]/gi, '') })}
                        className='w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm font-mono'
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className='flex gap-3 pt-4'>
              <Button
                variant='secondary'
                className='flex-1'
                onClick={() => setIsCheckoutOpen(false)}
              >
                Cancel
              </Button>
              <Button
                variant='primary'
                className='flex-1'
                onClick={handleCheckout}
                disabled={isProcessing}
              >
                {isProcessing ? 'Processing...' : 'Place Order'}
              </Button>
            </div>
          </div>
        </div>
      </Modal>

      {/* Success Modal */}
      <Modal
        isOpen={showSuccessModal}
        onClose={() => {
          setShowSuccessModal(false)
          navigate('/customer/orders')
        }}
        size='3xl'
        title="Order Successful!"
      >
        <div className='p-2 space-y-8'>
          <div className='text-center space-y-4'>
            <div className='w-20 h-20 bg-green-50 rounded-full flex items-center justify-center mx-auto'>
              <CheckCircle2 size={40} className='text-green-600 animate-bounce' />
            </div>
            <div>
              <h3 className='text-2xl font-bold text-gray-900'>Payment Received!</h3>
              <p className='text-gray-500 max-w-sm mx-auto mt-2'>
                Your order #{lastOrder?.order_id} has been placed successfully. 
                We've sent a confirmation email to {user?.email}.
              </p>
            </div>
          </div>

          <div className='bg-white shadow-sm border border-gray-100 rounded-xl overflow-hidden'>
             <Invoice order={lastOrder} user={user} />
          </div>

          <div className='flex justify-center pt-6'>
            <Button 
              variant='primary' 
              onClick={() => {
                setShowSuccessModal(false)
                navigate('/customer/orders')
              }}
              className='px-12'
            >
              Go to My Orders
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}

const CartItem = ({ item, onRemove, onUpdateQuantity }) => (
  <div className='bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition-shadow'>
    <div className='flex gap-4'>
      {/* Product Image */}
      <div className='w-24 h-24 bg-gray-50 rounded-lg overflow-hidden flex-shrink-0'>
        {item.images?.[0] ? (
          <img
            src={item.images[0]}
            alt={item.name}
            className='w-full h-full object-cover'
            onError={(e) => e.target.src = 'https://via.placeholder.com/100'}
          />
        ) : (
          <div className='w-full h-full flex items-center justify-center'>
            <ShoppingCart className='w-8 h-8 text-gray-300' />
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className='flex-1'>
        <div className='flex justify-between items-start'>
          <div>
            <h3 className='font-medium text-gray-900 hover:text-blue-600 transition-colors'>
              {item.name}
            </h3>
            <div className='flex flex-wrap gap-2 mt-1'>
              {item.selectedColor && (
                <span className='inline-flex items-center gap-1 text-xs text-gray-500'>
                  <span
                    className='w-2 h-2 rounded-full'
                    style={{ backgroundColor: item.selectedColor.toLowerCase().replace(' ', '') }}
                  />
                  {item.selectedColor}
                </span>
              )}
              {item.selectedSize && (
                <span className='text-xs text-gray-500'>
                  Size: {item.selectedSize}
                </span>
              )}
            </div>
          </div>
          <button
            onClick={() => onRemove(item.product_id, item.selectedColor, item.selectedSize)}
            className='p-1 text-gray-400 hover:text-red-500 transition-colors'
          >
            <Trash2 size={18} />
          </button>
        </div>

        <div className='flex justify-between items-end mt-4'>
          <div className='flex items-center gap-2'>
            <button
              onClick={() => onUpdateQuantity(item.product_id, item.quantity - 1, item.selectedColor, item.selectedSize)}
              className='w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors'
            >
              <Minus size={14} />
            </button>
            <span className='w-8 text-center text-sm font-medium'>{item.quantity}</span>
            <button
              onClick={() => onUpdateQuantity(item.product_id, item.quantity + 1, item.selectedColor, item.selectedSize)}
              className='w-8 h-8 flex items-center justify-center border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors'
            >
              <Plus size={14} />
            </button>
          </div>
          <div className='text-right'>
            <p className='text-lg font-semibold text-gray-900'>
              ${(item.discounted_price * item.quantity).toFixed(2)}
            </p>
            <p className='text-xs text-gray-400'>
              ${item.discounted_price.toFixed(2)} each
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
)