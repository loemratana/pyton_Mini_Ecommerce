import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from gui.theme import ModernTheme

class WishlistTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Header
        self.header = ctk.CTkLabel(self, text="My Favorites", font=ctk.CTkFont(size=22, weight="bold"))
        self.header.pack(anchor="w", padx=20, pady=(0, 20))

        # Treeview Container
        self.tree_frame = ctk.CTkFrame(self, corner_radius=10)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Centralized styling is already initialized in app.py via ModernTheme.setup_appearance()

        columns = ("ID", "Product Name", "Price", "Category", "In Stock")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=15)
        
        # Configure alternating row colors
        self.tree.tag_configure('oddrow', background=ModernTheme.BG_SECONDARY)
        self.tree.tag_configure('evenrow', background=ModernTheme.SURFACE)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Actions
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        self.add_cart_btn = ctk.CTkButton(btn_frame, text="Add to Cart", command=self.add_to_cart, state="disabled")
        self.add_cart_btn.pack(side="left", padx=10)
        
        self.remove_btn = ctk.CTkButton(btn_frame, text="Remove", fg_color="gray30", command=self.remove_wish, state="disabled")
        self.remove_btn.pack(side="left", padx=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh_table()

    def on_select(self, event):
        selected = self.tree.selection()
        state = "normal" if selected else "disabled"
        self.add_cart_btn.configure(state=state)
        self.remove_btn.configure(state=state)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        wish_ids = self.app.current_user.wishlist
        wish_products = [p for p in self.app.products if p.get_product_id() in wish_ids]
        
        for i, p in enumerate(wish_products):
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            val = (p.get_product_id(), p.get_name(), f"${p.get_discounted_price():.2f}", p.get_category(), p.get_stock())
            self.tree.insert("", tk.END, values=val, tags=(tag,))

    def add_to_cart(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        product = next((p for p in self.app.products if p.get_product_id() == pid), None)
        
        if product:
            success, msg = self.app.cart.add_item(product, 1)
            if success:
                messagebox.showinfo("Success", "Added to cart!")
                self.app.cart.save_cart()
                if hasattr(self.app, 'cart_tab'): self.app.cart_tab.refresh_table()
            else:
                messagebox.showerror("Error", msg)

    def remove_wish(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        
        if pid in self.app.current_user.wishlist:
            self.app.current_user.wishlist.remove(pid)
            # Save
            all_users = self.app.data_manager.load_users()
            for i, u in enumerate(all_users):
                if u.user_id == self.app.current_user.user_id:
                    all_users[i] = self.app.current_user
                    break
            self.app.data_manager.save_users(all_users)
            
            self.refresh_table()
            if hasattr(self.app, 'product_tab'): self.app.product_tab.refresh_table()
