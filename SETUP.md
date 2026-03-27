# Antigravity - Modern E-Commerce Web Application

A production-ready, full-stack e-commerce platform built with **React.js**, **Tailwind CSS**, and **Flask**. Features dual dashboards for Admin and Customer portals with a professional, modern UI/UX.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- npm or yarn

### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Flask server:**
   ```bash
   python app.py
   ```
   Server runs at `http://localhost:5000`

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```
   Application runs at `http://localhost:3000`

3. **Build for production:**
   ```bash
   npm run build
   ```

## 📁 Project Structure

```
project/
├── backend/
│   ├── app.py                 # Flask API server
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── UI.jsx         # Base components (Alert, Button, etc)
│   │   │   └── Layout.jsx     # Header & Sidebar
│   │   ├── pages/              # Page components
│   │   │   ├── Auth.jsx       # Login & Register
│   │   │   ├── admin/         # Admin dashboard pages
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── Products.jsx
│   │   │   │   ├── Orders.jsx
│   │   │   │   ├── Users.jsx
│   │   │   │   └── Analytics.jsx
│   │   │   └── customer/      # Customer dashboard pages
│   │   │       ├── Dashboard.jsx
│   │   │       ├── Shop.jsx
│   │   │       ├── Cart.jsx
│   │   │       └── Orders.jsx
│   │   ├── services/
│   │   │   └── apiService.js  # API calls
│   │   ├── store/
│   │   │   └── store.js       # Zustand store (auth & cart)
│   │   ├── App.jsx            # Main app & routing
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── models/                     # Python ORM models
├── data/                       # Data management
├── gui/                        # Original GUI (kept for reference)
└── README.md
```

## 🎯 Key Features

### Admin Dashboard
- **Dashboard**: Real-time analytics, revenue tracking, top products
- **Products Management**: CRUD operations with stock tracking
- **Order Management**: Track orders, update status
- **User Management**: View all customers and admins
- **Analytics**: Detailed insights, export reports (CSV/JSON)

### Customer Portal
- **Dashboard**: Quick stats, recent orders, featured products
- **Shop**: Browse products with filters, search, categories
- **Cart**: Add/remove items, quantity management, checkout
- **Orders**: View order history with details
- **Wishlist**: Save favorite products
- **Profile**: Account management

### Security & Authentication
- JWT token-based authentication
- Role-based access control (Admin/Customer)
- Password hashing with Werkzeug
- Token expiration handling
- Protected API endpoints

### UI/UX Features
✨ Modern gradient design
🎨 Tailwind CSS styling
📱 Fully responsive (mobile-first)
⚡ Smooth animations & transitions
🔔 Toast notifications
♿ Accessible components
🎭 Light/dark compatible

## 📊 API Endpoints

### Authentication
```
POST   /api/auth/register      # Register new user
POST   /api/auth/login          # Login & get JWT token
```

### Products
```
GET    /api/products            # Get all products
GET    /api/products/<id>       # Get single product
POST   /api/products            # Create product (Admin)
PUT    /api/products/<id>       # Update product (Admin)
DELETE /api/products/<id>       # Delete product (Admin)
GET    /api/products/by-category/<cat>  # Filter by category
```

### Orders
```
GET    /api/orders              # Get orders (all for Admin, user's for Customer)
POST   /api/orders              # Create new order
PUT    /api/orders/<id>         # Update order status (Admin)
```

### Users
```
GET    /api/users               # Get all users (Admin)
GET    /api/users/<id>          # Get user profile
PUT    /api/users/<id>          # Update user profile
```

### Analytics
```
GET    /api/analytics/dashboard # Get dashboard metrics (Admin)
```

### Wishlist
```
POST   /api/users/<id>/wishlist              # Add to wishlist
DELETE /api/users/<id>/wishlist/<product_id> # Remove from wishlist
```

## 🔐 Demo Credentials

Admin:
```
Email: admin@example.com
Password: password
```

Customer:
```
Email: customer@example.com
Password: password
```

## 🛠️ Technologies Used

### Frontend
- **React 18**: UI library
- **React Router v6**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **Axios**: HTTP client
- **Lucide React**: Icon library
- **React Hot Toast**: Notifications
- **Vite**: Build tool

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin requests
- **PyJWT**: JWT authentication
- **Werkzeug**: Security utilities
- **Python 3.8+**: Runtime

## 📈 Database Schema

### Users
```python
{
  user_id: string,
  name: string,
  email: string,
  password: string (hashed),
  role: "Admin" | "Customer",
  wishlist: [product_ids],
  status: "Active" | "Inactive",
  profile_image: string (optional)
}
```

### Products
```python
{
  product_id: string,
  name: string,
  price: float,
  stock: int,
  category: string,
  description: string,
  discount: float (0-100),
  image: string (optional),
  reviews: [{user, rating, comment}],
  created_at: datetime
}
```

### Orders
```python
{
  order_id: string,
  customer_name: string,
  items: [{product_id, name, price, quantity}],
  total: float,
  status: "Pending" | "Processing" | "Shipped" | "Delivered" | "Cancelled",
  order_date: datetime,
  discount: float,
  payment_method: string,
  shipping_address: string
}
```

## 🚀 Deployment

### Frontend Deployment (Vercel/Netlify)
```bash
npm run build
# Deploy the 'dist' folder
```

### Backend Deployment (Heroku/Railway)
```bash
# Set environment variables
# Deploy from backend directory
```

## 📝 Environment Variables

### Backend (.env)
```
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-secret-key-here
JWT_EXPIRATION_HOURS=24
```

### Frontend (.env.local)
```
VITE_API_URL=https://your-api-url.com
```

## 🐛 Troubleshooting

### CORS Issues
- Ensure Flask-CORS is enabled in backend
- Check API URL in frontend environment variables

### JWT Token Errors
- Verify token is transmitted in headers
- Check JWT expiration time
- Clear localStorage and re-login

### API Connection Failed
- Confirm backend is running on port 5000
- Check proxy settings in vite.config.js
- Verify API base URL

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Zustand Store](https://github.com/pmndrs/zustand)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

For issues or feature requests, please create an issue in the repository.

---

**Built with ❤️ for modern e-commerce experiences**
