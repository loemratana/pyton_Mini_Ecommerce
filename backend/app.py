"""
Flask Backend API for E-Commerce Application
Provides RESTful endpoints for React frontend
"""
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import json
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
import sys
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_manager import DataManager
from data.analytics import Analytics
from models.user import Admin, Customer
from models.product import Product
from models.order import Order
from models.category import Category
from models.cart import ShoppingCart

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_EXPIRATION_HOURS'] = 24

data_manager = DataManager()
analytics = Analytics(data_manager)

# Uploads Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        # Add timestamp to avoid collisions
        unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        file.save(os.path.join(UPLOAD_FOLDER, unique_name))
        return jsonify({
            'success': True, 
            'url': f'http://localhost:5000/uploads/{unique_name}'
        }), 200

# ==================== Authentication Routes ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'Customer')  # Default to Customer
        
        users = data_manager.load_users()
        
        # Check if email exists
        if any(u.email == email for u in users):
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        # Generate new user ID
        new_id = max([int(u.user_id) for u in users], default=0) + 1
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Create user
        if role == 'Admin':
            new_user = Admin(str(new_id), name, email, hashed_password)
        else:
            new_user = Customer(str(new_id), name, email, hashed_password)
        
        users.append(new_user)
        data_manager.save_users(users)
        
        # Generate JWT token for immediate login
        token = jwt.encode({
            'user_id': new_user.user_id,
            'email': new_user.email,
            'role': new_user.role,
            'name': new_user.name,
            'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS'])
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'token': token,
            'user': {
                'user_id': new_user.user_id,
                'name': new_user.name,
                'email': new_user.email,
                'role': new_user.role,
                'profile_image': getattr(new_user, 'profile_image', None),
                'wishlist': getattr(new_user, 'wishlist', [])
            }
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        users = data_manager.load_users()
        print(f"DEBUG: All loaded user emails: {[u.email for u in users]}", flush=True)
        user = next((u for u in users if u.email.lower() == email), None)
        
        print(f"DEBUG: Login attempt for email: {email}", flush=True)
        if not user:
            print(f"DEBUG: User not found for email: {email}", flush=True)
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Support both hashed and plain text passwords for legacy compatibility
        is_password_valid = False
        print(f"DEBUG: Stored password: {user.password}", flush=True)
        print(f"DEBUG: Received password: {password}", flush=True)
        
        if user.password.startswith('pbkdf2:sha256:'):
            is_password_valid = check_password_hash(user.password, password)
        else:
            is_password_valid = (user.password == password)
            
        print(f"DEBUG: Password valid: {is_password_valid}", flush=True)
        if not is_password_valid:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.user_id,
            'email': user.email,
            'role': user.role,
            'name': user.name,
            'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS'])
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'profile_image': user.profile_image,
                'wishlist': user.wishlist
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Middleware to verify JWT token
def verify_token(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'success': False, 'message': 'Token missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data['user_id']
            request.user_role = data['role']
            request.user_email = data['email']
            request.user_name = data['name']
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function


# ==================== Product Routes ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = data_manager.load_products()
        
        products_list = []
        for p in products:
            products_list.append({
                'product_id': p.get_product_id(),
                'name': p.get_name(),
                'price': p.get_price(),
                'stock': p.get_stock(),
                'category': p.get_category(),
                'description': p.get_description(),
                'discount': p.get_discount(),
                'discounted_price': p.get_discounted_price(),
                'image': p.get_image(),
                'images': p.get_images(),
                'colors': p.get_colors(),
                'sizes': p.get_sizes(),
                'reviews': p.get_reviews(),
                'average_rating': p.get_average_rating()
            })
        
        return jsonify({'success': True, 'products': products_list}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product"""
    try:
        products = data_manager.load_products()
        product = next((p for p in products if str(p.get_product_id()) == str(product_id)), None)
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        return jsonify({
            'success': True,
            'product': {
                'product_id': product.get_product_id(),
                'name': product.get_name(),
                'price': product.get_price(),
                'stock': product.get_stock(),
                'category': product.get_category(),
                'description': product.get_description(),
                'discount': product.get_discount(),
                'discounted_price': product.get_discounted_price(),
                'image': product.get_image(),
                'images': product.get_images(),
                'colors': product.get_colors(),
                'sizes': product.get_sizes(),
                'reviews': product.get_reviews(),
                'average_rating': product.get_average_rating()
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products/<product_id>/reviews', methods=['POST'])
@verify_token
def add_review(product_id):
    """Add a review to a product"""
    try:
        data = request.json
        rating = data.get('rating')
        comment = data.get('comment', '').strip()
        
        if not rating or not (1 <= int(rating) <= 5):
            return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
            
        products = data_manager.load_products()
        product = next((p for p in products if str(p.get_product_id()) == str(product_id)), None)
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
            
        # Create review object (dict style based on model)
        review = {
            'user_id': request.user_id,
            'user_name': request.user_name,
            'rating': int(rating),
            'comment': comment,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Add to product
        if not hasattr(product, 'reviews'):
            product.reviews = []
        product.reviews.append(review)
        
        data_manager.save_products(products)
        
        return jsonify({
            'success': True, 
            'message': 'Review added successfully',
            'review': review
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products', methods=['POST'])
@verify_token
def create_product():
    """Create new product (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.json
        products = data_manager.load_products()
        
        # Generate new product ID
        new_id = max([int(p.get_product_id()) for p in products], default=0) + 1
        
        new_product = Product(
            str(new_id),
            data.get('name'),
            data.get('price'),
            data.get('stock'),
            data.get('category'),
            data.get('description', ''),
            data.get('discount', 0),
            [], # reviews
            data.get('images', [data.get('image')]) if data.get('images') or data.get('image') else [],
            data.get('colors', []),
            data.get('sizes', [])
        )
        
        products.append(new_product)
        data_manager.save_products(products)
        
        return jsonify({
            'success': True,
            'message': 'Product created',
            'product_id': str(new_id)
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products/<product_id>', methods=['PUT'])
@verify_token
def update_product(product_id):
    """Update product (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.json
        products = data_manager.load_products()
        product = next((p for p in products if str(p.get_product_id()) == str(product_id)), None)
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        if 'name' in data:
            product.set_name(data['name'])
        if 'price' in data:
            product.set_price(data['price'])
        if 'stock' in data:
            product.set_stock(data['stock'])
        if 'category' in data:
            product.set_category(data['category'])
        if 'description' in data:
            product.set_description(data['description'])
        if 'discount' in data:
            product.set_discount(data['discount'])
        if 'images' in data:
            product.set_images(data['images'])
        elif 'image' in data:
            product.set_images([data['image']])
        if 'colors' in data:
            product.set_colors(data['colors'])
        if 'sizes' in data:
            product.set_sizes(data['sizes'])
        
        data_manager.save_products(products)
        
        return jsonify({
            'success': True,
            'message': 'Product updated'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products/<product_id>', methods=['DELETE'])
@verify_token
def delete_product(product_id):
    """Delete product (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        products = data_manager.load_products()
        products = [p for p in products if str(p.get_product_id()) != str(product_id)]
        data_manager.save_products(products)
        
        return jsonify({
            'success': True,
            'message': 'Product deleted'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products/<product_id>/reviews', methods=['POST'])
@verify_token
def add_review(product_id):
    """Add a review to a product"""
    try:
        data = request.json
        rating = data.get('rating')
        comment = data.get('comment', '')

        if not rating or not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
            return jsonify({'success': False, 'message': 'Valid rating between 1 and 5 is required'}), 400

        products = data_manager.load_products()
        product = next((p for p in products if str(p.get_product_id()) == str(product_id)), None)

        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404

        new_review = {
            'user_id': str(request.user_id),
            'user_name': request.user_name,
            'rating': float(rating),
            'comment': comment,
            'date': datetime.utcnow().isoformat()
        }

        product.add_review(new_review)
        data_manager.save_products(products)

        return jsonify({'success': True, 'message': 'Review added successfully'}), 201

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Order Routes ====================

@app.route('/api/orders', methods=['GET'])
@verify_token
def get_orders():
    """Get orders (all for Admin, only user's for Customer)"""
    try:
        orders = data_manager.load_orders()
        
        if request.user_role == 'Admin':
            orders_list = [o.summary('Admin') for o in orders]
        else:
            orders_list = [o.summary('Customer') for o in orders if o.customer_name == request.user_name]
        
        return jsonify({'success': True, 'orders': orders_list}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/orders', methods=['POST'])
@verify_token
def create_order():
    """Create new order"""
    try:
        data = request.json
        orders = data_manager.load_orders()
        
        # Generate new order ID (alphanumeric like 990B4CE5)
        new_id = uuid.uuid4().hex[:8].upper()
        
        # Determine initial status based on payment method
        initial_status = 'Pending' if data.get('payment_method') == 'cash' else 'Processing'

        new_order = Order(
            str(new_id),
            request.user_name,
            data.get('items'),
            data.get('total'),
            initial_status,
            None,
            data.get('discount', 0),
            data.get('payment_method', 'Cash'),
            data.get('shipping_address', ''),
            data.get('subtotal', 0.0),
            data.get('shipping', 0.0),
            data.get('tax', 0.0)
        )
        
        orders.append(new_order)
        data_manager.save_orders(orders)
        
        return jsonify({
            'success': True,
            'message': 'Order created',
            'order_id': str(new_id)
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/orders/<order_id>', methods=['PUT'])
@verify_token
def update_order_status(order_id):
    """Update order status (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.json
        orders = data_manager.load_orders()
        order = next((o for o in orders if o.order_id == order_id), None)
        
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'}), 404
        
        order.status = data.get('status', order.status)
        data_manager.save_orders(orders)
        
        return jsonify({
            'success': True,
            'message': 'Order updated'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== User Routes ====================

@app.route('/api/users', methods=['GET'])
@verify_token
def get_users():
    """Get all users (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        users = data_manager.load_users()
        users_list = []
        
        for u in users:
            users_list.append({
                'user_id': u.user_id,
                'name': u.name,
                'email': u.email,
                'role': u.role,
                'status': u.status,
                'profile_image': u.profile_image,
                'wishlist_count': len(u.wishlist)
            })
        
        return jsonify({'success': True, 'users': users_list}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users/<user_id>', methods=['GET'])
@verify_token
def get_user(user_id):
    """Get user profile"""
    try:
        users = data_manager.load_users()
        user = next((u for u in users if u.user_id == user_id), None)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Users can only view their own profile unless they're admin
        if request.user_role != 'Admin' and request.user_id != user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        return jsonify({
            'success': True,
            'user': {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'status': user.status,
                'profile_image': user.profile_image,
                'wishlist': user.wishlist
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users/<user_id>', methods=['PUT'])
@verify_token
def update_user(user_id):
    """Update user profile"""
    try:
        data = request.json
        users = data_manager.load_users()
        user = next((u for u in users if u.user_id == user_id), None)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Users can only update their own profile unless they're admin
        if request.user_role != 'Admin' and request.user_id != user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        if 'name' in data:
            user.name = data['name']
        if 'profile_image' in data:
            user.profile_image = data['profile_image']
        if 'status' in data and request.user_role == 'Admin':
            user.status = data['status']
        
        data_manager.save_users(users)
        
        return jsonify({
            'success': True,
            'message': 'User updated'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users/<user_id>', methods=['DELETE'])
@verify_token
def delete_user(user_id):
    """Delete user (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        users = data_manager.load_users()
        user_to_delete = next((u for u in users if u.user_id == user_id), None)
        
        if not user_to_delete:
            return jsonify({'success': False, 'message': 'User not found'}), 404
            
        # Optional: Prevent admin from deleting themselves
        if user_id == request.user_id:
            return jsonify({'success': False, 'message': 'Cannot delete your own admin account'}), 400

        users = [u for u in users if u.user_id != user_id]
        data_manager.save_users(users)
        
        return jsonify({'success': True, 'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Wishlist Routes ====================

@app.route('/api/users/<user_id>/wishlist', methods=['POST'])
@verify_token
def add_to_wishlist(user_id):
    """Add product to wishlist"""
    try:
        if request.user_role != 'Admin' and str(request.user_id) != str(user_id):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.json
        product_id = data.get('product_id')
        
        users = data_manager.load_users()
        user = next((u for u in users if str(u.user_id) == str(user_id)), None)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        if product_id not in user.wishlist:
            user.wishlist.append(product_id)
            data_manager.save_users(users)
        
        return jsonify({
            'success': True,
            'message': 'Added to wishlist'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/users/<user_id>/wishlist/<product_id>', methods=['DELETE'])
@verify_token
def remove_from_wishlist(user_id, product_id):
    """Remove product from wishlist"""
    try:
        if request.user_role != 'Admin' and str(request.user_id) != str(user_id):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        users = data_manager.load_users()
        user = next((u for u in users if str(u.user_id) == str(user_id)), None)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        if product_id in user.wishlist:
            user.wishlist.remove(product_id)
            data_manager.save_users(users)
        
        return jsonify({
            'success': True,
            'message': 'Removed from wishlist'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Analytics Routes ====================

@app.route('/api/analytics/dashboard', methods=['GET'])
@verify_token
def get_dashboard_analytics():
    """Get dashboard analytics (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        summary = analytics.get_dashboard_summary()
        
        return jsonify({
            'success': True,
            'analytics': summary
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = data_manager.load_categories()
        categories_list = []
        for c in categories:
            categories_list.append({
                'category_id': c.get_category_id(),
                'name': c.get_name(),
                'description': c.get_description(),
                'image': c.get_image()
            })
        return jsonify({'success': True, 'categories': categories_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/categories', methods=['POST'])
@verify_token
def create_category():
    """Create new category (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        data = request.json
        if not data.get('name'):
            return jsonify({'success': False, 'message': 'Name is required'}), 400
            
        categories = data_manager.load_categories()
        
        # Check if exists
        if any(c.get_name().lower() == data['name'].lower() for c in categories):
            return jsonify({'success': False, 'message': 'Category already exists'}), 400
            
        new_id = max([int(c.get_category_id()) for c in categories], default=0) + 1
        new_cat = Category(str(new_id), data['name'], data.get('description', ''), data.get('image', ''))
        
        categories.append(new_cat)
        data_manager.save_categories(categories)
        
        return jsonify({'success': True, 'message': 'Category created'}), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/categories/<cat_id>', methods=['PUT'])
@verify_token
def update_category(cat_id):
    """Update category (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
            
        data = request.json
        categories = data_manager.load_categories()
        category = next((c for c in categories if str(c.get_category_id()) == str(cat_id)), None)
        
        if not category:
            return jsonify({'success': False, 'message': 'Category not found'}), 404
            
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        # Update image if it's explicitly passed in the data payload
        if 'image' in data:
            category.image = data.get('image')
        
        data_manager.save_categories(categories)
        return jsonify({'success': True, 'message': 'Category updated'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/categories/<cat_id>', methods=['DELETE'])
@verify_token
def delete_category(cat_id):
    """Delete category (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
            
        categories = data_manager.load_categories()
        categories = [c for c in categories if str(c.get_category_id()) != str(cat_id)]
        data_manager.save_categories(categories)
        
        return jsonify({'success': True, 'message': 'Category deleted'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/products/by-category/<category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category"""
    try:
        products = data_manager.load_products()
        filtered = [p for p in products if p.get_category().lower() == category.lower()]
        
        products_list = []
        for p in filtered:
            products_list.append({
                'product_id': p.get_product_id(),
                'name': p.get_name(),
                'price': p.get_price(),
                'stock': p.get_stock(),
                'category': p.get_category(),
                'description': p.get_description(),
                'discount': p.get_discount(),
                'discounted_price': p.get_discounted_price(),
                'image': p.get_image(),
                'images': p.get_images(),
                'colors': p.get_colors(),
                'sizes': p.get_sizes(),
                'reviews': p.get_reviews(),
                'average_rating': p.get_average_rating()
            })
        
        return jsonify({'success': True, 'products': products_list}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Change Password ====================

@app.route('/api/auth/change-password', methods=['POST'])
@verify_token
def change_password():
    """Change user password"""
    try:
        data = request.json
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({'success': False, 'message': 'Both current and new password required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'success': False, 'message': 'New password must be at least 6 characters'}), 400
        
        users = data_manager.load_users()
        user = next((u for u in users if u.user_id == request.user_id), None)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Verify current password
        if user.password.startswith('pbkdf2:sha256:'):
            if not check_password_hash(user.password, current_password):
                return jsonify({'success': False, 'message': 'Current password is incorrect'}), 401
        else:
            if user.password != current_password:
                return jsonify({'success': False, 'message': 'Current password is incorrect'}), 401
        
        # Set new password
        user.password = generate_password_hash(new_password)
        data_manager.save_users(users)
        
        return jsonify({'success': True, 'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Cancel Order ====================

@app.route('/api/orders/<order_id>/cancel', methods=['PUT'])
@verify_token
def cancel_order(order_id):
    """Cancel an order (Customer can cancel their own pending/processing orders)"""
    try:
        orders = data_manager.load_orders()
        order = next((o for o in orders if o.order_id == order_id), None)
        
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'}), 404
        
        # Check ownership (unless admin)
        if request.user_role != 'Admin' and order.customer_name != request.user_name:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Only allow cancellation of Pending or Processing orders
        if order.status not in ['Pending', 'Processing']:
            return jsonify({'success': False, 'message': f'Cannot cancel order with status: {order.status}'}), 400
        
        order.status = 'Cancelled'
        data_manager.save_orders(orders)
        
        # Restore stock for cancelled items
        products = data_manager.load_products()
        for item in order.items:
            product = next((p for p in products if str(p.get_product_id()) == str(item.get('product_id', ''))), None)
            if product:
                product.set_stock(product.get_stock() + item.get('quantity', 0))
        data_manager.save_products(products)
        
        return jsonify({'success': True, 'message': 'Order cancelled successfully'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Coupon / Promo Code System ====================

# Simple in-memory coupon store (in production, this would be in DB)
COUPONS = {
    'WELCOME10': {'discount_percent': 10, 'min_order': 0, 'max_uses': 999, 'active': True, 'description': '10% off for new members'},
    'SAVE20': {'discount_percent': 20, 'min_order': 50, 'max_uses': 100, 'active': True, 'description': '20% off on orders over $50'},
    'FREESHIP': {'discount_percent': 0, 'min_order': 0, 'max_uses': 999, 'active': True, 'free_shipping': True, 'description': 'Free shipping on any order'},
    'SPRING25': {'discount_percent': 25, 'min_order': 100, 'max_uses': 50, 'active': True, 'description': '25% off spring sale'},
}

@app.route('/api/coupons/validate', methods=['POST'])
@verify_token
def validate_coupon():
    """Validate and apply a coupon code"""
    try:
        data = request.json
        code = data.get('code', '').strip().upper()
        subtotal = data.get('subtotal', 0)
        
        if not code:
            return jsonify({'success': False, 'message': 'Coupon code is required'}), 400
        
        coupon = COUPONS.get(code)
        
        if not coupon:
            return jsonify({'success': False, 'message': 'Invalid coupon code'}), 404
        
        if not coupon.get('active', False):
            return jsonify({'success': False, 'message': 'This coupon has expired'}), 400
        
        if subtotal < coupon.get('min_order', 0):
            return jsonify({
                'success': False, 
                'message': f'Minimum order of ${coupon["min_order"]} required for this coupon'
            }), 400
        
        discount_amount = (subtotal * coupon['discount_percent']) / 100
        free_shipping = coupon.get('free_shipping', False)
        
        return jsonify({
            'success': True,
            'coupon': {
                'code': code,
                'discount_percent': coupon['discount_percent'],
                'discount_amount': round(discount_amount, 2),
                'free_shipping': free_shipping,
                'description': coupon['description']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/coupons', methods=['GET'])
@verify_token
def get_coupons():
    """Get all active coupons (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        coupons_list = []
        for code, details in COUPONS.items():
            coupons_list.append({
                'code': code,
                **details
            })
        
        return jsonify({'success': True, 'coupons': coupons_list}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Export Report ====================

@app.route('/api/analytics/export', methods=['GET'])
@verify_token
def export_report():
    """Export sales report as Excel (Admin only)"""
    try:
        if request.user_role != 'Admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sales_report.xlsx')
        success, message = analytics.export_to_excel(save_path)
        
        if success:
            return send_from_directory(
                os.path.dirname(save_path), 
                'sales_report.xlsx', 
                as_attachment=True,
                download_name=f'sales_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
            )
        else:
            return jsonify({'success': False, 'message': message}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
