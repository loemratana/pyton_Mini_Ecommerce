from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, name, email, password, role, wishlist=None, status="Active", profile_image=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.wishlist = wishlist if wishlist else [] # List of product IDs
        self.status = status
        self.profile_image = profile_image


    @abstractmethod
    def view_products(self, products):
        """View products - polymorphic behavior"""
        pass

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "wishlist": self.wishlist,
            "status": self.status,
            "profile_image": self.profile_image
        }



class Admin(User):
    def __init__(self, user_id, name, email, password, wishlist=None, status="Active", profile_image=None):
        super().__init__(user_id, name, email, password, "Admin", wishlist, status, profile_image)

    def view_products(self, products):
        """Admin sees: ID, name, price, stock, category, discount"""
        view = []
        for p in products:
            view.append({
                "ID": p.get_product_id(),
                "Name": p.get_name(),
                "Price": p.get_price(),
                "Stock": p.get_stock(),
                "Category": p.get_category(),
                "Discount": p.get_discount()
            })
        return view

class Customer(User):
    def __init__(self, user_id, name, email, password, wishlist=None, status="Active", profile_image=None):
        super().__init__(user_id, name, email, password, "Customer", wishlist, status, profile_image)

    def view_products(self, products):
        """Customer sees: name, price, discounted price (if available)"""
        view = []
        for p in products:
            view.append({
                "ID": p.get_product_id(),
                "Name": p.get_name(),
                "Price": p.get_price(),
                "Category": p.get_category(),
                "Stock": p.get_stock(),
                "In Wishlist": "❤️" if p.get_product_id() in self.wishlist else "🤍"
            })
        return view

