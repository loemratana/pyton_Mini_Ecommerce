# ⚡ Quick Reference Guide - Antigravity E-Commerce

Quick commands and reference for developers.

## 🚀 Start Development

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Visit:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`

---

## 📁 File Locations

```
Project Structure:
├── backend/
│   ├── app.py              # Main Flask app
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/App.jsx         # Main React component
│   ├── src/pages/          # All page components
│   ├── src/components/     # Reusable components
│   ├── src/store/store.js  # Zustand state management
│   └── src/services/       # API calls
├── models/                 # Data models (Python classes)
├── data/                   # Data manager
└── gui/                    # Original GUI (reference)
```

---

## 🔑 Demo Credentials

| Type | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | password |
| Customer | customer@example.com | password |

---

## 🧭 Navigate Application

### Admin Routes
- Dashboard: `/admin`
- Products: `/admin/products`
- Orders: `/admin/orders`
- Users: `/admin/users`
- Analytics: `/admin/analytics`
- Settings: `/admin/settings`

### Customer Routes
- Dashboard: `/customer`
- Shop: `/customer/shop`
- Cart: `/customer/cart`
- Orders: `/customer/orders`
- Wishlist: `/customer/wishlist`
- Profile: `/customer/profile`

### Auth Routes
- Login: `/login`
- Register: `/register`

---

## 🔧 Common Tasks

### Add New Page

1. Create file: `frontend/src/pages/[role]/NewPage.jsx`
2. Import in `App.jsx`
3. Add route:
```jsx
<Route path='/admin/newpage' element={
  <ProtectedRoute requiredRole='Admin'>
    <AdminLayout><NewPage /></AdminLayout>
  </ProtectedRoute>
} />
```

### Add New API Endpoint

1. Add function in `backend/app.py`
2. Add route decorator: `@app.route('/api/endpoint', methods=['GET/POST'])`
3. Add JWT verification if needed: `@verify_token`
4. Add client function in `frontend/src/services/apiService.js`

### Style Components

Use Tailwind CSS classes:
```jsx
<div className='container mx-auto px-4 py-8'>
  <h1 className='text-3xl font-bold text-gray-900'>Title</h1>
  <p className='text-gray-600 mt-2'>Description</p>
</div>
```

Predefined classes in `index.css`:
- `.btn` `.btn-primary` `.btn-secondary` `.btn-danger`
- `.card` - Styled container
- `.input` - Form input
- `.badge` `.badge-primary` `.badge-success`

---

## 📡 API Quick Reference

```javascript
// Import service
import { apiService } from '../services/apiService'

// Use in component
const response = await apiService.getProducts()
const response = await apiService.login({ email, password })
const response = await apiService.createProduct(data)

// Handle response
if (response.data.success) {
  // Success
} else {
  // Error
}
```

---

## 🎨 Component Templates

### Loading State
```jsx
import { Spinner } from '../components/UI'
if (loading) return <Spinner />
```

### Alert Message
```jsx
import { Alert } from '../components/UI'
{error && <Alert type='error' message={error} />}
```

### Button
```jsx
import { Button } from '../components/UI'
<Button variant='primary' onClick={handleClick}>
  Click Me
</Button>
```

### Modal
```jsx
import { Modal, Button } from '../components/UI'
<Modal 
  isOpen={isOpen}
  title='Modal Title'
  onClose={() => setIsOpen(false)}
  actions={[
    <Button key='cancel' onClick={() => setIsOpen(false)}>Cancel</Button>,
    <Button key='save' variant='primary' onClick={handleSave}>Save</Button>
  ]}
>
  <div>Modal content</div>
</Modal>
```

---

## 🛠️ Debugging

### Browser DevTools
- React: Use React Developer Tools extension
- Network: Check API calls in Network tab
- Console: Check for errors

### Backend Debugging
```python
# Print debug info
print(f"Debug: {variable}")

# Check Flask logs
# Errors appear in terminal where you ran `python app.py`

# Test endpoint with curl
curl -X GET http://localhost:5000/api/products \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Redux DevTools (Zustand)
```javascript
// Add to store to see state changes
import { devtools } from 'zustand/middleware'
```

---

## 📦 Dependencies

### Frontend (key packages)
```json
{
  "react": "^18.2.0",
  "react-router-dom": "^6.15.0",
  "axios": "^1.5.0",
  "zustand": "^4.4.1",
  "tailwindcss": "^3.3.5"
}
```

### Backend (key packages)
```
Flask==2.3.3
Flask-CORS==4.0.0
PyJWT==2.8.1
Werkzeug==2.3.7
```

---

## 🚀 Build & Deploy

### Build Frontend
```bash
cd frontend
npm run build
# Creates 'dist' folder with production build
```

### Deploy Frontend (Vercel)
```bash
npm install -g vercel
vercel --prod
```

### Deploy Backend (Heroku)
```bash
heroku create app-name
git push heroku main
```

---

## 🐛 Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| Port already in use | Kill process: `lsof -ti:3000 \| xargs kill -9` |
| CORS error | Check API URL in `.env` |
| JWT error | Clear localStorage, re-login |
| 404 error | Check route path spelling |
| Blank page | Check browser console for errors |
| Slow performance | Check Network tab, optimize images |

---

## 🎯 Environment Setup

### Create .env files

**frontend/.env.local:**
```
VITE_API_URL=http://localhost:5000
```

**backend/.env:**
```
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=dev-secret-key
JWT_EXPIRATION_HOURS=24
```

---

## 📊 Database

Current: JSON files
- `products.txt` - Product data
- `users.txt` - User data
- `orders.txt` - Order data
- `categories.txt` - Category data

---

## 🔐 Security Checklist

- [ ] Change demo credentials
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Validate all user inputs
- [ ] Use environment variables
- [ ] Keep dependencies updated
- [ ] Review API permissions

---

## 💡 Performance Tips

1. Use React.memo for expensive components
2. Implement code splitting for routes
3. Cache API responses
4. Optimize images
5. Use CSS classes instead of inline styles
6. Lazy load components
7. Monitor bundle size: `npm run build -- --analyze`

---

## 📚 Useful Links

- [React Docs](https://react.dev)
- [Tailwind Docs](https://tailwindcss.com/docs)
- [Flask Docs](https://flask.palletsprojects.com)
- [Zustand Docs](https://github.com/pmndrs/zustand)
- [Axios Docs](https://axios-http.com)

---

## ✅ Pre-Commit Checklist

- [ ] Code runs without errors
- [ ] All tests pass
- [ ] No console.log debugging code
- [ ] Variables named clearly
- [ ] Comments for complex logic
- [ ] No hardcoded values
- [ ] Follows code style

---

**Last Updated:** 2024
**Version:** 1.0.0
