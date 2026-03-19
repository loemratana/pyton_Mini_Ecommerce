from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

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
            "role": self.role
        }

class Admin(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, "Admin")

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
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, "Customer")

    def view_products(self, products):
        """Customer sees: name, price, discounted price (if available)"""
        view = []
        for p in products:
            view.append({
                "ID": p.get_product_id(),
                "Name": p.get_name(),
                "Price": p.get_price(),
                "Discounted Price": p.get_discounted_price(),
                "Category": p.get_category(),
                "Stock": p.get_stock()
            })
        return view
