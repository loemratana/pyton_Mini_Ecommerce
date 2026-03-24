import json
import os
from models.product import Product
from models.order import Order
from models.user import Admin, Customer
from models.category import Category


class DataManager:
    def __init__(self, products_file="products.txt", orders_file="orders.txt", users_file="users.txt", categories_file="categories.txt"):
        self.products_file = products_file
        self.orders_file = orders_file
        self.users_file = users_file
        self.categories_file = categories_file

        
    def load_products(self):
        if not os.path.exists(self.products_file):
            return []
        try:
            with open(self.products_file, "r") as f:
                data = json.load(f)
                return [Product.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_products(self, products):
        data = [p.to_dict() for p in products]
        with open(self.products_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_orders(self):
        if not os.path.exists(self.orders_file):
            return []
        try:
            with open(self.orders_file, "r") as f:
                data = json.load(f)
                return [Order.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_orders(self, orders):
        data = [o.to_dict() for o in orders]
        with open(self.orders_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_users(self):
        if not os.path.exists(self.users_file):
            return []
        try:
            with open(self.users_file, "r") as f:
                data = json.load(f)
                users = []
                for item in data:
                    w = item.get("wishlist", [])
                    s = item.get("status", "Active")
                    img = item.get("profile_image", None)
                    if item["role"] == "Admin":
                        users.append(Admin(item["user_id"], item["name"], item["email"], item["password"], wishlist=w, status=s, profile_image=img))
                    else:
                        users.append(Customer(item["user_id"], item["name"], item["email"], item["password"], wishlist=w, status=s, profile_image=img))
                return users


        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_users(self, users):
        data = [u.to_dict() for u in users]
        with open(self.users_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_categories(self):
        if not os.path.exists(self.categories_file):
            return []
        try:
            with open(self.categories_file, "r") as f:
                data = json.load(f)
                return [Category.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_categories(self, categories):
        data = [c.to_dict() for c in categories]
        with open(self.categories_file, "w") as f:
            json.dump(data, f, indent=4)

