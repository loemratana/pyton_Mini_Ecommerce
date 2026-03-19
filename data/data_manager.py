import json
import os
from models.product import Product
from models.order import Order
from models.user import Admin, Customer

class DataManager:
    def __init__(self, products_file="products.txt", orders_file="orders.txt", users_file="users.txt"):
        self.products_file = products_file
        self.orders_file = orders_file
        self.users_file = users_file
        
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
                    if item["role"] == "Admin":
                        users.append(Admin(item["user_id"], item["name"], item["email"], item["password"]))
                    else:
                        users.append(Customer(item["user_id"], item["name"], item["email"], item["password"]))
                return users
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_users(self, users):
        data = [u.to_dict() for u in users]
        with open(self.users_file, "w") as f:
            json.dump(data, f, indent=4)
