import React from 'react'
import { Package, MapPin, CreditCard, Calendar, ShoppingBag, Download, Printer, CheckCircle, Truck } from 'lucide-react'
import { Button } from './UI'

export const Invoice = ({ order, user }) => {
  if (!order) return null

  const handlePrint = () => {
    window.print()
  }

  const formatDate = (date) => {
    return new Date(date || Date.now()).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const calculateSubtotal = () => {
    if (order.subtotal) return order.subtotal
    if (order.items) {
      return order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
    }
    return order.total - (order.tax || 0) - (order.shipping || 0)
  }

  return (
    <div className='bg-white max-w-4xl mx-auto' id='invoice-content'>
      {/* Header */}
      <div className='border-b border-gray-200 pb-6 mb-6'>
        <div className='flex justify-between items-start'>
          <div>
            <div className='flex items-center gap-3 mb-4'>
              <div className='w-10 h-10 bg-gray-900 rounded-lg flex items-center justify-center'>
                <ShoppingBag className='text-white' size={20} />
              </div>
              <span className='text-xl font-semibold text-gray-900'>Antigravity Store</span>
            </div>
            <div className='text-sm text-gray-500 space-y-1'>
              <p>123 Innovation Drive</p>
              <p>Silicon Valley, CA 94025</p>
              <p>support@antigravity.com</p>
            </div>
          </div>
          <div className='text-right'>
            <h1 className='text-3xl font-light text-gray-900 mb-2'>INVOICE</h1>
            <p className='text-sm font-medium text-gray-500'>Order #{order.order_id}</p>
            <div className='flex items-center justify-end gap-1 text-sm text-gray-500 mt-1'>
              <Calendar size={14} />
              <span>{formatDate(order.order_date)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Order Status */}
      {order.status && (
        <div className='bg-gray-50 rounded-lg p-4 mb-6'>
          <div className='flex items-center gap-2'>
            {order.status === 'Delivered' || order.status === 'Completed' ? (
              <CheckCircle size={18} className='text-green-500' />
            ) : (
              <Truck size={18} className='text-blue-500' />
            )}
            <span className='text-sm font-medium text-gray-700'>Order Status:</span>
            <span className={`text-sm font-semibold ${order.status === 'Delivered' || order.status === 'Completed'
              ? 'text-green-600'
              : 'text-blue-600'
              }`}>
              {order.status}
            </span>
          </div>
        </div>
      )}

      {/* Addresses */}
      <div className='grid grid-cols-1 md:grid-cols-2 gap-8 mb-8'>
        <div>
          <h3 className='text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3'>
            Billed To
          </h3>
          <div className='space-y-1'>
            <p className='font-medium text-gray-900'>{user?.name || order.customer_name}</p>
            <p className='text-sm text-gray-600'>{user?.email || 'customer@example.com'}</p>
          </div>
        </div>
        <div>
          <h3 className='text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3'>
            Shipping Address
          </h3>
          <div className='flex gap-2 text-sm text-gray-600'>
            <MapPin size={16} className='text-gray-400 flex-shrink-0 mt-0.5' />
            <p>{order.shipping_address || 'No address provided'}</p>
          </div>
        </div>
      </div>

      {/* Payment Method */}
      {order.payment_method && (
        <div className='mb-8'>
          <div className='flex items-center gap-2 text-sm text-gray-600'>
            <CreditCard size={16} className='text-gray-400' />
            <span className='font-medium'>Payment Method:</span>
            <span className='capitalize'>{order.payment_method}</span>
          </div>
        </div>
      )}

      {/* Items Table */}
      <div className='mb-8'>
        <table className='w-full text-left'>
          <thead>
            <tr className='border-b border-gray-200'>
              <th className='pb-3 text-xs font-semibold text-gray-400 uppercase tracking-wider'>
                Product
              </th>
              <th className='pb-3 text-xs font-semibold text-gray-400 uppercase tracking-wider text-center'>
                Quantity
              </th>
              <th className='pb-3 text-xs font-semibold text-gray-400 uppercase tracking-wider text-right'>
                Price
              </th>
              <th className='pb-3 text-xs font-semibold text-gray-400 uppercase tracking-wider text-right'>
                Total
              </th>
            </tr>
          </thead>
          <tbody className='divide-y divide-gray-100'>
            {order.items?.map((item, idx) => (
              <tr key={idx}>
                <td className='py-4'>
                  <p className='font-medium text-gray-900'>{item.name}</p>
                  {(item.color || item.size) && (
                    <p className='text-xs text-gray-500 mt-1'>
                      {item.color && `Color: ${item.color}`}
                      {item.color && item.size && ' • '}
                      {item.size && `Size: ${item.size}`}
                    </p>
                  )}
                </td>
                <td className='py-4 text-center text-gray-600'>
                  {item.quantity}
                </td>
                <td className='py-4 text-right text-gray-600'>
                  ${item.price?.toFixed(2)}
                </td>
                <td className='py-4 text-right font-medium text-gray-900'>
                  ${(item.price * item.quantity).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Summary */}
      <div className='flex justify-end mb-8'>
        <div className='w-72 space-y-2'>
          <div className='flex justify-between text-sm'>
            <span className='text-gray-600'>Subtotal</span>
            <span className='text-gray-900'>${calculateSubtotal().toFixed(2)}</span>
          </div>
          {order.shipping > 0 && (
            <div className='flex justify-between text-sm'>
              <span className='text-gray-600'>Shipping</span>
              <span className='text-gray-900'>${order.shipping.toFixed(2)}</span>
            </div>
          )}
          {order.tax > 0 && (
            <div className='flex justify-between text-sm'>
              <span className='text-gray-600'>Tax</span>
              <span className='text-gray-900'>${order.tax.toFixed(2)}</span>
            </div>
          )}
          <div className='pt-2 border-t border-gray-200 flex justify-between'>
            <span className='text-base font-semibold text-gray-900'>Total</span>
            <span className='text-xl font-bold text-gray-900'>${order.total.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className='pt-6 border-t border-gray-200 text-center'>
        <p className='text-sm text-gray-500'>
          Thank you for your purchase!
        </p>
        <p className='text-xs text-gray-400 mt-1'>
          If you have any questions, contact us at support@antigravity.com
        </p>
      </div>

      {/* Action Buttons */}
      <div className='mt-8 flex justify-center gap-3 print:hidden'>
        <Button variant='secondary' onClick={handlePrint} className='gap-2'>
          <Printer size={16} />
          Print Invoice
        </Button>
        <Button variant='primary' className='gap-2'>
          <Download size={16} />
          Download PDF
        </Button>
      </div>

      {/* Print Styles */}
      <style>{`
        @media print {
          body * {
            visibility: hidden;
          }
          #invoice-content, #invoice-content * {
            visibility: visible;
          }
          #invoice-content {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            padding: 20px;
          }
          .print\\:hidden {
            display: none !important;
          }
          button {
            display: none !important;
          }
        }
      `}</style>
    </div>
  )
}