import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from models.user import Admin, Customer
from gui.theme import ModernTheme
from PIL import Image
import os

class ProductTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=ModernTheme.BG_PRIMARY)
        self.app = app
        self.filtered_products = []
        self.is_admin = isinstance(self.app.current_user, Admin)
        
        # Setup directories
        self.images_dir = "assets/product_images"
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header section
        self._create_header(main_container)
        
        # Toolbar with search & filters
        self._create_toolbar(main_container)

        # Toolbar Card with modern styling
        self.toolbar_frame = ModernTheme.create_modern_card(main_container)
        self.toolbar_frame.pack(fill="x", pady=(0, 20))
        
        toolbar_content = ctk.CTkFrame(self.toolbar_frame, fg_color="transparent")
        toolbar_content.pack(fill="x", padx=20, pady=15)
        
        # Search section
        search_frame = ctk.CTkFrame(toolbar_content, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search products...", 
                                          width=250, height=40,
                                          fg_color=ModernTheme.SURFACE,
                                          border_color=ModernTheme.BORDER,
                                          border_width=1,
                                          text_color=ModernTheme.TEXT_PRIMARY)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # View toggle (Table/Grid)
        self.view_var = tk.StringVar(value="table")
        table_radio = ctk.CTkRadioButton(search_frame, text="📊 Table", variable=self.view_var, 
                                         value="table", command=self.switch_view,
                                         text_color=ModernTheme.TEXT_PRIMARY)
        table_radio.pack(side="left", padx=10)
        
        grid_radio = ctk.CTkRadioButton(search_frame, text="🔲 Grid", variable=self.view_var, 
                                        value="grid", command=self.switch_view,
                                        text_color=ModernTheme.TEXT_PRIMARY)
        grid_radio.pack(side="left", padx=10)

        # Sort dropdown
        self.sort_combo = ctk.CTkOptionMenu(search_frame, values=["None", "Price (Low-High)", "Price (High-Low)", "Rating (High-Low)"],
                                            command=self.on_sort,
                                            fg_color=ModernTheme.SURFACE,
                                            button_color=ModernTheme.PRIMARY,
                                            text_color=ModernTheme.TEXT_PRIMARY)
        self.sort_combo.set("📊 Sort")
        self.sort_combo.pack(side="left", padx=(10, 15))

        # Filter section - Row 2 of toolbar
        filter_frame = ctk.CTkFrame(toolbar_content, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(filter_frame, text="🔽 Filters:", text_color=ModernTheme.TEXT_PRIMARY,
                    font=ModernTheme.get_label_font()).pack(side="left", padx=(0, 10))
        
        # Category filter
        self.cat_filter_combo = ctk.CTkOptionMenu(filter_frame, values=["All Categories"] + [c.name for c in self.app.categories],
                                                  command=self.on_filter,
                                                  fg_color=ModernTheme.SURFACE,
                                                  button_color=ModernTheme.PRIMARY,
                                                  text_color=ModernTheme.TEXT_PRIMARY,
                                                  width=180)
        self.cat_filter_combo.set("All Categories")
        self.cat_filter_combo.pack(side="left", padx=5)
        
        # Stock filter
        self.stock_filter_combo = ctk.CTkOptionMenu(filter_frame, values=["All Stock", "In Stock", "Low Stock", "Out of Stock"],
                                                    command=self.on_filter,
                                                    fg_color=ModernTheme.SURFACE,
                                                    button_color=ModernTheme.PRIMARY,
                                                    text_color=ModernTheme.TEXT_PRIMARY,
                                                    width=140)
        self.stock_filter_combo.set("All Stock")
        self.stock_filter_combo.pack(side="left", padx=5)
        
        # Rating filter
        self.rating_filter_combo = ctk.CTkOptionMenu(filter_frame, values=["All Ratings", "4★ & above", "3★ & above", "Unrated"],
                                                     command=self.on_filter,
                                                     fg_color=ModernTheme.SURFACE,
                                                     button_color=ModernTheme.PRIMARY,
                                                     text_color=ModernTheme.TEXT_PRIMARY,
                                                     width=140)
        self.rating_filter_combo.set("All Ratings")
        self.rating_filter_combo.pack(side="left", padx=5)
        
        # Clear filters button
        clear_btn = ModernTheme.create_modern_button(filter_frame, "❌ Clear Filters", 
                                                     command=self.clear_filters, color="secondary", height=40, width=120)
        clear_btn.pack(side="left", padx=(15, 0))

        # Action buttons section
        button_frame = ctk.CTkFrame(toolbar_content, fg_color="transparent")
        button_frame.pack(side="right", fill="x")
        
        if isinstance(self.app.current_user, Admin):
            self.add_btn = ModernTheme.create_modern_button(button_frame, "✨ Add Product", 
                                                            command=self.add_product, color="success", height=40, width=140)
            self.add_btn.pack(side="right", padx=(10, 0))
            
            self.del_btn = ModernTheme.create_modern_button(button_frame, "🗑️ Delete", 
                                                            command=self.delete_product, color="danger", height=40, width=95)
            self.del_btn.pack(side="right", padx=5)
            self.del_btn.configure(state="disabled")

            self.edit_btn = ModernTheme.create_modern_button(button_frame, "✏️ Edit", 
                                                             command=self.edit_product, color="primary", height=40, width=95)
            self.edit_btn.pack(side="right", padx=5)
            self.edit_btn.configure(state="disabled")

            self.view_rev_btn = ModernTheme.create_modern_button(button_frame, "⭐ Reviews", 
                                                                 command=self.view_product_reviews, color="primary", height=40, width=95)
            self.view_rev_btn.pack(side="right", padx=5)
            self.view_rev_btn.configure(state="disabled")

        else:
            self.add_cart_btn = ModernTheme.create_modern_button(button_frame, "🛒 Add to Cart", 
                                                                 command=self.add_to_cart, color="success", height=40, width=140)
            self.add_cart_btn.pack(side="right", padx=(10, 0))
            self.add_cart_btn.configure(state="disabled")

            self.review_btn = ModernTheme.create_modern_button(button_frame, "⭐ Review", 
                                                               command=self.add_product_review, color="primary", height=40, width=95)
            self.review_btn.pack(side="right", padx=5)
            self.review_btn.configure(state="disabled")

            self.wish_btn = ctk.CTkButton(button_frame, text="❤️ Wishlist", height=40, width=95,
                                          fg_color="transparent", border_width=2, border_color=ModernTheme.PRIMARY,
                                          text_color=ModernTheme.PRIMARY, hover_color=ModernTheme.SURFACE_HOVER,
                                          command=self.toggle_wishlist, font=ModernTheme.get_label_font())
            self.wish_btn.pack(side="right", padx=5)
            self.wish_btn.configure(state="disabled")

        # Content container with table and grid views
        self.content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        # TABLE VIEW
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background=ModernTheme.SURFACE, 
                        foreground=ModernTheme.TEXT_PRIMARY, 
                        fieldbackground=ModernTheme.SURFACE,
                        borderwidth=0,
                        font=("Segoe UI", 11))
        style.map("Treeview", 
                  background=[('selected', ModernTheme.PRIMARY)],
                  foreground=[('selected', ModernTheme.TEXT_PRIMARY)])
        style.configure("Treeview.Heading", 
                        background=ModernTheme.BG_SECONDARY, 
                        foreground=ModernTheme.TEXT_PRIMARY, 
                        borderwidth=0,
                        font=("Segoe UI", 12, "bold"))

        # Treeview Container
        self.table_frame_container = ModernTheme.create_modern_card(self.content_container)
        
        columns = ("ID", "Name", "Price", "Category", "Stock", "Rating") if isinstance(self.app.current_user, Admin) else ("ID", "Name", "Price", "Discounted Price", "Category", "Stock", "Rating", "Status")

        self.tree = ttk.Treeview(self.table_frame_container, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # GRID VIEW
        self.grid_frame_container = ModernTheme.create_modern_card(self.content_container)
        
        self.grid_scroll_frame = ctk.CTkScrollableFrame(self.grid_frame_container, fg_color="transparent")
        self.grid_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.grid_container = ctk.CTkFrame(self.grid_scroll_frame, fg_color="transparent")
        self.grid_container.pack(fill="x")
        
        # Initialize with table view
        self.switch_view()
        self.refresh_table()

    def switch_view(self):
        if self.view_var.get() == "table":
            self.table_frame_container.pack(fill="both", expand=True)
            self.grid_frame_container.pack_forget()
        else:
            self.table_frame_container.pack_forget()
            self.grid_frame_container.pack(fill="both", expand=True)
            self.refresh_grid()

    def refresh_grid(self):
        # Clear existing grid items
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        
        # Reset grid configuration
        self.grid_container.grid_columnconfigure((0, 1), weight=0)
        
        if not self.filtered_products:
            empty_label = ctk.CTkLabel(self.grid_container, text="No products found", 
                                      text_color=ModernTheme.TEXT_SECONDARY, font=ModernTheme.get_label_font())
            empty_label.pack(pady=50)
            return
        
        # Create 2-column grid
        for idx, product in enumerate(self.filtered_products):
            row = idx // 2
            col = idx % 2
            
            # Product card
            card = ModernTheme.create_modern_card(self.grid_container, corner_radius=12)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            card_content = ctk.CTkFrame(card, fg_color="transparent")
            card_content.pack(fill="both", expand=True, padx=15, pady=15)
            
            # Product name
            name_label = ctk.CTkLabel(card_content, text=product.get_name(), 
                                     font=ModernTheme.get_subtitle_font(),
                                     text_color=ModernTheme.TEXT_PRIMARY)
            name_label.pack(anchor="w", pady=(0, 8))
            
            # Category badge
            cat_badge = ctk.CTkLabel(card_content, text=f"📁 {product.get_category()}", 
                                    font=ModernTheme.get_small_font(),
                                    text_color=ModernTheme.TEXT_SECONDARY)
            cat_badge.pack(anchor="w", pady=(0, 8))
            
            # Price section
            price_frame = ctk.CTkFrame(card_content, fg_color="transparent")
            price_frame.pack(fill="x", pady=(0, 8))
            
            if isinstance(self.app.current_user, Admin):
                price_text = f"💰 ${product.get_price():.2f}"
            else:
                discount = product.get_discount()
                discounted = product.get_price() * (1 - discount / 100)
                if discount > 0:
                    price_text = f"💰 ${discounted:.2f}  ~~${product.get_price():.2f}~~  ({discount}'.' off)"
                else:
                    price_text = f"💰 ${product.get_price():.2f}"
            
            price_label = ctk.CTkLabel(price_frame, text=price_text, 
                                      font=ModernTheme.get_label_font(),
                                      text_color=ModernTheme.SUCCESS if discount > 0 else ModernTheme.TEXT_PRIMARY)
            price_label.pack(anchor="w")
            
            # Stock status
            stock = product.get_stock()
            if stock == 0:
                stock_color = ModernTheme.DANGER
                stock_text = "🔴 Out of Stock"
            elif stock < 10:
                stock_color = ModernTheme.WARNING
                stock_text = f"🟡 Low Stock ({stock})"
            else:
                stock_color = ModernTheme.SUCCESS
                stock_text = f"🟢 In Stock ({stock})"
            
            stock_label = ctk.CTkLabel(card_content, text=stock_text, 
                                      font=ModernTheme.get_small_font(),
                                      text_color=stock_color)
            stock_label.pack(anchor="w", pady=(0, 8))
            
            # Rating
            avg_rating = product.get_average_rating()
            rating_text = f"⭐ {avg_rating:.1f}" if avg_rating > 0 else "⭐ No ratings"
            rating_label = ctk.CTkLabel(card_content, text=rating_text, 
                                       font=ModernTheme.get_small_font(),
                                       text_color=ModernTheme.INFO)
            rating_label.pack(anchor="w", pady=(0, 12))
            
            # Divider
            divider = ctk.CTkFrame(card_content, height=1, fg_color=ModernTheme.BORDER)
            divider.pack(fill="x", pady=(8, 12))
            
            # Action buttons
            btn_frame = ctk.CTkFrame(card_content, fg_color="transparent")
            btn_frame.pack(fill="x")
            
            if isinstance(self.app.current_user, Admin):
                edit_btn = ctk.CTkButton(btn_frame, text="✏️ Edit", height=32, font=ModernTheme.get_small_font(),
                                        fg_color=ModernTheme.PRIMARY, hover_color=ModernTheme.PRIMARY_HOVER,
                                        command=lambda p=product: self._open_product_form(p))
                edit_btn.pack(side="left", padx=(0, 5), expand=True, fill="both")
                
                del_btn = ctk.CTkButton(btn_frame, text="🗑️ Delete", height=32, font=ModernTheme.get_small_font(),
                                       fg_color=ModernTheme.DANGER, hover_color=ModernTheme.DANGER_HOVER,
                                       command=lambda p=product: self._delete_product_grid(p))
                del_btn.pack(side="left", expand=True, fill="both")
            else:
                cart_btn = ctk.CTkButton(btn_frame, text="🛒 Cart", height=32, font=ModernTheme.get_small_font(),
                                        fg_color=ModernTheme.SUCCESS, hover_color=ModernTheme.SUCCESS_HOVER,
                                        command=lambda p=product: self._add_to_cart_grid(p))
                cart_btn.pack(side="left", padx=(0, 5), expand=True, fill="both")
                
                wish_btn = ctk.CTkButton(btn_frame, text="❤️ Wish", height=32, font=ModernTheme.get_small_font(),
                                        fg_color=ModernTheme.PRIMARY, hover_color=ModernTheme.PRIMARY_HOVER,
                                        command=lambda p=product: self._toggle_wishlist_grid(p))
                wish_btn.pack(side="left", expand=True, fill="both")

    def on_search(self, event):
        self.refresh_table()
        
    def on_sort(self, choice):
        self.refresh_table()
    
    def on_filter(self, choice):
        self.refresh_table()
    
    def clear_filters(self):
        self.search_entry.delete(0, tk.END)
        self.cat_filter_combo.set("All Categories")
        self.stock_filter_combo.set("All Stock")
        self.rating_filter_combo.set("All Ratings")
        self.sort_combo.set("📊 Sort")
        self.refresh_table()

    def refresh_table(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        query = self.search_entry.get().lower()
        sort_val = self.sort_combo.get()
        cat_filter = self.cat_filter_combo.get()
        stock_filter = self.stock_filter_combo.get()
        rating_filter = self.rating_filter_combo.get()
        
        if not self.app.products:
            self.filtered_products = []
            if self.view_var.get() == "grid":
                self.refresh_grid()
            return
            
        view_data = self.app.current_user.view_products(self.app.products)
        
        # Apply search filter
        if query:
            view_data = [d for d in view_data if query in str(d["Name"]).lower() or query in str(d["Category"]).lower()]
        
        # Apply category filter
        if cat_filter != "All Categories":
            view_data = [d for d in view_data if d["Category"] == cat_filter]
        
        # Apply stock filter
        if stock_filter == "In Stock":
            view_data = [d for d in view_data if d["Stock"] > 0]
        elif stock_filter == "Low Stock":
            view_data = [d for d in view_data if 0 < d["Stock"] < 10]
        elif stock_filter == "Out of Stock":
            view_data = [d for d in view_data if d["Stock"] == 0]
        
        # Apply rating filter
        if rating_filter == "4★ & above":
            view_data = [d for d in view_data if next((p for p in self.app.products if p.get_product_id() == d["ID"]), None).get_average_rating() >= 4]
        elif rating_filter == "3★ & above":
            view_data = [d for d in view_data if next((p for p in self.app.products if p.get_product_id() == d["ID"]), None).get_average_rating() >= 3]
        elif rating_filter == "Unrated":
            view_data = [d for d in view_data if next((p for p in self.app.products if p.get_product_id() == d["ID"]), None).get_average_rating() == 0]
        
        # Apply sorting
        if sort_val == "Price (Low-High)":
            if isinstance(self.app.current_user, Admin):
                view_data.sort(key=lambda x: float(x["Price"]))
            else:
                view_data.sort(key=lambda x: float(x["Discounted Price"]))
        elif sort_val == "Price (High-Low)":
            if isinstance(self.app.current_user, Admin):
                view_data.sort(key=lambda x: float(x["Price"]), reverse=True)
            else:
                view_data.sort(key=lambda x: float(x["Discounted Price"]), reverse=True)
        elif sort_val == "Rating (High-Low)":
            view_data.sort(key=lambda x: next((p for p in self.app.products if p.get_product_id() == x["ID"]), None).get_average_rating(), reverse=True)

        # Store filtered products for grid view
        self.filtered_products = [next((p for p in self.app.products if p.get_product_id() == d["ID"]), None) for d in view_data]

        # Populate treeview
        for d in view_data:
            avg_rating = next((p for p in self.app.products if p.get_product_id() == d["ID"]), None).get_average_rating()
            rating_str = f"⭐ {avg_rating:.1f}" if avg_rating > 0 else "N/A"
            
            if isinstance(self.app.current_user, Admin):
                values = (d["ID"], d["Name"], f"${d['Price']:.2f}", d["Category"], d["Stock"], rating_str)
            else:
                values = (d["ID"], d["Name"], f"${d['Price']:.2f}", f"${d['Discounted Price']:.2f}", d["Category"], d["Stock"], rating_str, d["In Wishlist"])
            self.tree.insert("", tk.END, values=values)
        
        # Refresh grid if in grid view
        if self.view_var.get() == "grid":
            self.refresh_grid()



    def on_select(self, event):
        selected = self.tree.selection()
        if hasattr(self, 'edit_btn'):
            self.edit_btn.configure(state="normal" if selected else "disabled")
        if hasattr(self, 'del_btn'):
            self.del_btn.configure(state="normal" if selected else "disabled")
        if hasattr(self, 'add_cart_btn'):
            self.add_cart_btn.configure(state="normal" if selected else "disabled")
        if hasattr(self, 'wish_btn'):
            self.wish_btn.configure(state="normal" if selected else "disabled")
        if hasattr(self, 'review_btn'):
            self.review_btn.configure(state="normal" if selected else "disabled")
        if hasattr(self, 'view_rev_btn'):
            self.view_rev_btn.configure(state="normal" if selected else "disabled")

    def _delete_product_grid(self, product):
        """Delete product from grid view"""
        if messagebox.askyesno("Confirm", f"Delete '{product.get_name()}'?"):
            self.app.products = [p for p in self.app.products if p.get_product_id() != product.get_product_id()]
            self.app.data_manager.save_products(self.app.products)
            self.refresh_table()

    def _add_to_cart_grid(self, product):
        """Add to cart from grid view"""
        qty_window = ctk.CTkToplevel(self)
        qty_window.title("Select Quantity")
        qty_window.geometry("300x200")
        qty_window.attributes("-topmost", True)
        qty_window.configure(fg_color=ModernTheme.BG_PRIMARY)
        
        ctk.CTkLabel(qty_window, text=f"Adding: {product.get_name()}", font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(pady=10)
        ctk.CTkLabel(qty_window, text="Quantity:", text_color=ModernTheme.TEXT_PRIMARY).pack()
        qty_entry = ctk.CTkEntry(qty_window, fg_color=ModernTheme.SURFACE, border_color=ModernTheme.BORDER, border_width=1)
        qty_entry.insert(0, "1")
        qty_entry.pack(pady=10)
        
        def confirm():
            try:
                q = int(qty_entry.get())
                success, msg = self.app.cart.add_item(product, q)
                if success:
                    messagebox.showinfo("Success", msg)
                    self.app.cart.save_cart()
                    qty_window.destroy()
                    if hasattr(self.app, 'cart_tab'): self.app.cart_tab.refresh_table()
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        ModernTheme.create_modern_button(qty_window, "Add to Cart", command=confirm, color="success").pack(pady=10)

    def _toggle_wishlist_grid(self, product):
        """Toggle wishlist from grid view"""
        user = self.app.current_user
        if product.get_product_id() in user.wishlist:
            user.wishlist.remove(product.get_product_id())
            msg = "Removed from wishlist."
        else:
            user.wishlist.append(product.get_product_id())
            msg = "Added to wishlist."
        
        # Save users
        all_users = self.app.data_manager.load_users()
        for i, u in enumerate(all_users):
            if u.user_id == user.user_id:
                all_users[i] = user
                break
        self.app.data_manager.save_users(all_users)
        
        self.refresh_table()
        if hasattr(self.app, 'wishlist_tab'): self.app.wishlist_tab.refresh_table()
        messagebox.showinfo("Wishlist", msg)




    def _open_product_form(self, product=None):
        form = ctk.CTkToplevel(self)
        form.title("✏️ Manage Product" if product else "✨ Add New Product")
        form.geometry("500x650")
        form.configure(fg_color=ModernTheme.BG_PRIMARY)
        form.attributes("-topmost", True)
        
        # Main container
        main_frame = ctk.CTkFrame(form, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        title_text = "Edit Product Details" if product else "Create New Product"
        title = ctk.CTkLabel(main_frame, text=title_text,
                            font=ModernTheme.get_title_font(),
                            text_color=ModernTheme.PRIMARY)
        title.pack(anchor="w", pady=(0, 25))

        # Input form card
        form_card = ModernTheme.create_modern_card(main_frame)
        form_card.pack(fill="both", expand=True)
        
        input_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        input_frame.pack(padx=25, pady=25, fill="both", expand=True)

        # Name field
        ctk.CTkLabel(input_frame, text="Product Name",
                     font=ModernTheme.get_label_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        name_entry = ctk.CTkEntry(input_frame, width=300, height=45, 
                                  placeholder_text="e.g., Wireless Headphones",
                                  fg_color=ModernTheme.SURFACE,
                                  border_color=ModernTheme.BORDER,
                                  border_width=1)
        name_entry.insert(0, product.get_name() if product else "")
        name_entry.pack(pady=(0, 15))
        
        # Price field
        ctk.CTkLabel(input_frame, text="Price ($)",
                     font=ModernTheme.get_label_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        price_entry = ctk.CTkEntry(input_frame, width=300, height=45,
                                   placeholder_text="0.00",
                                   fg_color=ModernTheme.SURFACE,
                                   border_color=ModernTheme.BORDER,
                                   border_width=1)
        price_entry.insert(0, str(product.get_price()) if product else "0.0")
        price_entry.pack(pady=(0, 15))
        
        # Stock field
        ctk.CTkLabel(input_frame, text="Stock Quantity",
                     font=ModernTheme.get_label_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        stock_entry = ctk.CTkEntry(input_frame, width=300, height=45,
                                   placeholder_text="0",
                                   fg_color=ModernTheme.SURFACE,
                                   border_color=ModernTheme.BORDER,
                                   border_width=1)
        stock_entry.insert(0, str(product.get_stock()) if product else "0")
        stock_entry.pack(pady=(0, 15))
        
        # Category Dropdown
        ctk.CTkLabel(input_frame, text="Category",
                     font=ModernTheme.get_label_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        category_options = [c.name for c in self.app.categories] if self.app.categories else ["General"]
        cat_var = tk.StringVar(value=product.get_category() if product else category_options[0])
        self.cat_dropdown = ctk.CTkOptionMenu(input_frame, variable=cat_var, values=category_options, 
                                              width=300, height=45,
                                              fg_color=ModernTheme.SURFACE,
                                              button_color=ModernTheme.PRIMARY,
                                              text_color=ModernTheme.TEXT_PRIMARY)
        self.cat_dropdown.pack(pady=(0, 15))

        # Discount field
        ctk.CTkLabel(input_frame, text="Discount (%)",
                     font=ModernTheme.get_label_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        disc_entry = ctk.CTkEntry(input_frame, width=300, height=45,
                                  placeholder_text="0",
                                  fg_color=ModernTheme.SURFACE,
                                  border_color=ModernTheme.BORDER,
                                  border_width=1)
        disc_entry.insert(0, str(product.get_discount()) if product else "0")
        disc_entry.pack(pady=(0, 25))

        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        def save():
            try:
                name = name_entry.get().strip()
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                category = self.cat_dropdown.get()
                discount = float(disc_entry.get())

                if not name:
                    messagebox.showwarning("Invalid", "Product name cannot be empty")
                    return

                if product:
                    product.set_name(name)
                    product.set_price(price)
                    product.set_stock(stock)
                    product.set_category(category)
                    product.set_discount(discount)
                else:
                    from models.product import Product
                    new_id = max([p.get_product_id() for p in self.app.products], default=0) + 1
                    new_p = Product(new_id, name, price, stock, category, "", discount)
                    self.app.products.append(new_p)
                
                self.app.data_manager.save_products(self.app.products)
                self.refresh_table()
                form.destroy()
            except ValueError as e:
                messagebox.showerror("Invalid Input", "Please check all numerical fields")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn = ModernTheme.create_modern_button(button_frame, "💾 Save Product",
                                                    command=save, color="success", width=300, height=50)
        save_btn.pack(side="left")

    def add_product(self):
        self._open_product_form()
        
    def edit_product(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        product = next((p for p in self.app.products if p.get_product_id() == pid), None)
        if product:
            self._open_product_form(product)

    def delete_product(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            self.app.products = [p for p in self.app.products if p.get_product_id() != pid]
            self.app.data_manager.save_products(self.app.products)
            self.refresh_table()

    def add_to_cart(self):
        selected = self.tree.selection()
        if not selected: return
            
        item = self.tree.item(selected[0])
        pid = item['values'][0]
        product = next((p for p in self.app.products if p.get_product_id() == pid), None)
        
        if product:
            qty_window = ctk.CTkToplevel(self)
            qty_window.title("Select Quantity")
            qty_window.geometry("300x200")
            qty_window.attributes("-topmost", True)
            
            ctk.CTkLabel(qty_window, text=f"Adding: {product.get_name()}", font=("Roboto", 14)).pack(pady=10)
            ctk.CTkLabel(qty_window, text="Quantity:").pack()
            qty_entry = ctk.CTkEntry(qty_window)
            qty_entry.insert(0, "1")
            qty_entry.pack(pady=10)
            
            def confirm():
                try:
                    q = int(qty_entry.get())
                    success, msg = self.app.cart.add_item(product, q)
                    if success:
                        messagebox.showinfo("Success", msg)
                        self.app.cart.save_cart()
                        qty_window.destroy()
                        if hasattr(self.app, 'cart_tab'): self.app.cart_tab.refresh_table()
                    else:
                        messagebox.showerror("Error", msg)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number")
                    
            ctk.CTkButton(qty_window, text="Add to Cart", command=confirm).pack(pady=10)

    def toggle_wishlist(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        
        user = self.app.current_user
        if pid in user.wishlist:
            user.wishlist.remove(pid)
            msg = "Removed from wishlist."
        else:
            user.wishlist.append(pid)
            msg = "Added to wishlist."
            
        # Save users
        all_users = self.app.data_manager.load_users()
        for i, u in enumerate(all_users):
            if u.user_id == user.user_id:
                all_users[i] = user
                break
        self.app.data_manager.save_users(all_users)
        
        self.refresh_table()
        if hasattr(self.app, 'wishlist_tab'): self.app.wishlist_tab.refresh_table()
        messagebox.showinfo("Wishlist", msg)

    def add_product_review(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        product = next((p for p in self.app.products if p.get_product_id() == pid), None)
        
        if product:
            rev_win = ctk.CTkToplevel(self)
            rev_win.title(f"Review: {product.get_name()}")
            rev_win.geometry("400x450")
            rev_win.attributes("-topmost", True)
            
            ctk.CTkLabel(rev_win, text="Product Review", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
            
            # Rating
            ctk.CTkLabel(rev_win, text="Rating (1-5):").pack(pady=(10, 5))
            rating_slider = ctk.CTkSlider(rev_win, from_=1, to=5, number_of_steps=4)
            rating_slider.set(5)
            rating_slider.pack(pady=5)
            
            # Comment
            ctk.CTkLabel(rev_win, text="Your Feedback:").pack(pady=(10, 5))
            comment_box = ctk.CTkTextbox(rev_win, height=100)
            comment_box.pack(pady=5, padx=20, fill="x")
            
            def submit():
                rating = int(rating_slider.get())
                comment = comment_box.get("1.0", "end-1c")
                if not comment:
                    return messagebox.showwarning("Missing", "Please provide feedback.")
                
                product.add_review(self.app.current_user.name, rating, comment)
                self.app.data_manager.save_products(self.app.products)
                self.refresh_table()
                rev_win.destroy()
                messagebox.showinfo("Success", "Review submitted!")
            
            ctk.CTkButton(rev_win, text="Submit Review", command=submit).pack(pady=30)

    def view_product_reviews(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        product = next((p for p in self.app.products if p.get_product_id() == pid), None)
        
        if product:
            vr_win = ctk.CTkToplevel(self)
            vr_win.title(f"Reviews for {product.get_name()}")
            vr_win.geometry("500x500")
            vr_win.attributes("-topmost", True)
            
            ctk.CTkLabel(vr_win, text=f"Customer Feedback", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
            
            rev_box = ctk.CTkTextbox(vr_win, height=350)
            rev_box.pack(pady=10, padx=20, fill="both", expand=True)
            
            reviews = product.get_reviews()
            content = ""
            for r in reviews:
                content += f"👤 {r['user']}  |  {'⭐' * r['rating']}\n"
                content += f"   \"{r['comment']}\"\n"
                content += "--------------------------------------------\n"
            
            rev_box.insert("1.0", content if content else "No reviews yet for this product.")
            rev_box.configure(state="disabled")
            
            ctk.CTkButton(vr_win, text="Close", command=vr_win.destroy).pack(pady=20)


