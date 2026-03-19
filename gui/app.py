import tkinter as tk
from tkinter import ttk
from models.user import Admin, Customer
from models.cart import ShoppingCart
from gui.product_tab import ProductTab
from gui.cart_tab import CartTab
from gui.order_tab import OrderTab
from gui.report_tab import ReportTab
from gui.profile_tab import ProfileTab

class ECommerceApp:
    def __init__(self, root, data_manager, analytics, current_user):
        self.root = root
        self.root.title("E-Commerce System")
        self.root.geometry("900x600")
        
        self.data_manager = data_manager
        self.analytics = analytics
        self.current_user = current_user
        
        self.products = self.data_manager.load_products()
        self.orders = self.data_manager.load_orders()
        self.cart = ShoppingCart()
        
        try:
            import json, os
            if os.path.exists("cart.json"):
                with open("cart.json") as f:
                    cdata = json.load(f)
                    for item in cdata:
                        pid = item["product_id"]
                        qty = item["quantity"]
                        p = next((x for x in self.products if x.get_product_id() == pid), None)
                        if p:
                            self.cart.add_item(p, qty)
        except Exception as e:
            pass

        self._setup_ui()

    def _setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.product_tab = ProductTab(self.notebook, self)
        self.notebook.add(self.product_tab, text="Products")

        if not isinstance(self.current_user, Admin):
            self.cart_tab = CartTab(self.notebook, self)
            self.notebook.add(self.cart_tab, text="Shopping Cart")

        self.order_tab = OrderTab(self.notebook, self)
        self.notebook.add(self.order_tab, text="Orders")

        if isinstance(self.current_user, Admin):
            self.report_tab = ReportTab(self.notebook, self)
            self.notebook.add(self.report_tab, text="Reports")

        self.profile_tab = ProfileTab(self.notebook, self)
        self.notebook.add(self.profile_tab, text="Profile")
        
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.refresh_tabs())

    def refresh_tabs(self):
        if hasattr(self, 'product_tab'): self.product_tab.refresh_table()
        if hasattr(self, 'cart_tab'): self.cart_tab.refresh_table()
        if hasattr(self, 'order_tab'): self.order_tab.refresh_table()
        if hasattr(self, 'report_tab'): self.report_tab.refresh_data()
