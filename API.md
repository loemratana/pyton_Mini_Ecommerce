# 📚 API Documentation - Antigravity E-Commerce Platform

Complete REST API documentation for the Antigravity e-commerce backend.

## 🔗 Base URL
```
http://localhost:5000/api
```

## 🔐 Authentication

All endpoints (except `/auth/login` and `/auth/register`) require JWT token in header:

```
Authorization: Bearer <your-jwt-token>
```

---

## 🔑 Authentication Endpoints

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "Customer"  // "Admin" or "Customer"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Registration successful",
  "user_id": "1"
}
```

---

### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "user_id": "1",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "Customer",
    "profile_image": null,
    "wishlist": ["1", "3"]
  }
}
```

**Error (401):**
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

---

## 📦 Product Endpoints

### Get All Products
```http
GET /products
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "products": [
    {
      "product_id": "1",
      "name": "Product Name",
      "price": 99.99,
      "stock": 50,
      "category": "Electronics",
      "description": "Product description",
      "discount": 10,
      "discounted_price": 89.99,
      "image": "/path/to/image.jpg",
      "reviews": [
        {
          "user": "John",
          "rating": 5,
          "comment": "Great product!"
        }
      ],
      "average_rating": 4.5
    }
  ]
}
```

---

### Get Single Product
```http
GET /products/1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "product": {
    "product_id": "1",
    "name": "Product Name",
    ... // same as list
  }
}
```

---

### Create Product (Admin Only)
```http
POST /products
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "name": "New Product",
  "price": 99.99,
  "stock": 100,
  "category": "Electronics",
  "description": "Product description",
  "discount": 10,
  "image": "/path/to/image.jpg"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Product created",
  "product_id": "42"
}
```

---

### Update Product (Admin Only)
```http
PUT /products/1
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "name": "Updated Name",
  "price": 79.99,
  "stock": 75,
  "discount": 15
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Product updated"
}
```

---

### Delete Product (Admin Only)
```http
DELETE /products/1
Authorization: Bearer <admin-token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Product deleted"
}
```

---

### Get Products by Category
```http
GET /products/by-category/Electronics
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "products": [...]
}
```

---

## 🛒 Order Endpoints

### Get Orders
```http
GET /orders
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "orders": [
    {
      "order_id": "1",
      "customer": "John Doe",
      "items": [
        {
          "name": "Product 1",
          "quantity": 2
        }
      ],
      "total": 199.99,
      "status": "Pending",
      "order_date": "2024-01-15 10:30:00"
    }
  ]
}
```

**Note:** Admins see all orders, customers see only their own.

---

### Create Order
```http
POST /orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "items": [
    {
      "product_id": "1",
      "name": "Product Name",
      "price": 99.99,
      "quantity": 2
    }
  ],
  "total": 199.98,
  "payment_method": "Card",
  "shipping_address": "123 Main St, City, State 12345",
  "discount": 0
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Order created",
  "order_id": "42"
}
```

---

### Update Order Status (Admin Only)
```http
PUT /orders/1
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "status": "Shipped"
}
```

**Valid statuses:** Pending, Processing, Shipped, Delivered, Cancelled

**Response (200):**
```json
{
  "success": true,
  "message": "Order updated"
}
```

---

## 👥 User Endpoints

### Get All Users (Admin Only)
```http
GET /users
Authorization: Bearer <admin-token>
```

**Response (200):**
```json
{
  "success": true,
  "users": [
    {
      "user_id": "1",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "Customer",
      "status": "Active",
      "profile_image": null,
      "wishlist_count": 3
    }
  ]
}
```

---

### Get User Profile
```http
GET /users/1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "user": {
    "user_id": "1",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "Customer",
    "status": "Active",
    "profile_image": null,
    "wishlist": ["1", "3", "5"]
  }
}
```

---

### Update User Profile
```http
PUT /users/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Doe",
  "profile_image": "/path/to/image.jpg"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "User updated"
}
```

---

## ❤️ Wishlist Endpoints

### Add to Wishlist
```http
POST /users/1/wishlist
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": "5"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Added to wishlist"
}
```

---

### Remove from Wishlist
```http
DELETE /users/1/wishlist/5
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Removed from wishlist"
}
```

---

## 📊 Analytics Endpoints

### Get Dashboard Analytics (Admin Only)
```http
GET /analytics/dashboard
Authorization: Bearer <admin-token>
```

**Response (200):**
```json
{
  "success": true,
  "analytics": {
    "total_revenue": 5234.50,
    "total_orders": 45,
    "total_products": 120,
    "total_customers": 87,
    "status_breakdown": {
      "Pending": 5,
      "Processing": 8,
      "Shipped": 25,
      "Delivered": 7
    },
    "top_products": [
      ["1", 45],
      ["2", 38],
      ["3", 32]
    ]
  }
}
```

---

## 📂 Categories Endpoints

### Get All Categories
```http
GET /categories
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "categories": [
    {
      "category_id": "1",
      "name": "Electronics",
      "description": "Electronic devices"
    }
  ]
}
```

---

## 🏥 Health Check

### System Health
```http
GET /health
```

**Response (200):**
```json
{
  "status": "healthy"
}
```

---

## ❌ Error Handling

### Common Error Responses

**401 Unauthorized:**
```json
{
  "success": false,
  "message": "Token missing" / "Invalid token" / "Token expired"
}
```

**403 Forbidden:**
```json
{
  "success": false,
  "message": "Unauthorized"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "message": "Product not found" / "User not found"
}
```

**400 Bad Request:**
```json
{
  "success": false,
  "message": "Invalid request data"
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "message": "Internal server error"
}
```

---

## 🔄 Request/Response Flow

### Typical Customer Flow

1. **Register/Login**
   ```
   POST /auth/register or /auth/login
   ↓ Get JWT token
   ```

2. **Browse Products**
   ```
   GET /products
   ↓ Get all products
   ```

3. **Add to Wishlist**
   ```
   POST /users/{id}/wishlist
   ↓ Save favorite products
   ```

4. **Create Order**
   ```
   POST /orders
   ↓ Place order
   ```

5. **View Orders**
   ```
   GET /orders
   ↓ See order history
   ```

---

## 📝 Data Models

### User Model
```json
{
  "user_id": "string",
  "name": "string",
  "email": "string",
  "password": "string (hashed)",
  "role": "Admin | Customer",
  "wishlist": ["product_id"],
  "status": "Active | Inactive",
  "profile_image": "string (optional)"
}
```

### Product Model
```json
{
  "product_id": "string",
  "name": "string",
  "price": "float",
  "stock": "integer",
  "category": "string",
  "description": "string",
  "discount": "float (0-100)",
  "image": "string (optional)",
  "reviews": [{"user", "rating", "comment"}],
  "average_rating": "float"
}
```

### Order Model
```json
{
  "order_id": "string",
  "customer_name": "string",
  "items": [{"product_id", "name", "price", "quantity"}],
  "total": "float",
  "status": "Pending | Processing | Shipped | Delivered | Cancelled",
  "order_date": "datetime",
  "discount": "float",
  "payment_method": "string",
  "shipping_address": "string"
}
```

---

## ⚡ Rate Limiting (Optional)

Recommended rate limits per IP:
- **Authentication:** 5 requests/minute
- **API Calls:** 100 requests/minute
- **File Upload:** 10 requests/minute

---

## 🔒 Security Headers

All responses include:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

---

**API Version:** 1.0.0
**Last Updated:** 2024
**Status:** Production Ready ✅
