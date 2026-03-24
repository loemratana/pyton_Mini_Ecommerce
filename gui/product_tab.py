import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from models.user import Admin, Customer
from gui.theme import ModernTheme
from PIL import Image
import os
import shutil

class ProductTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=ModernTheme.BG_PRIMARY)
        self.app = app
        self.filtered_products = []
        self.is_admin = isinstance(self.app.current_user, Admin)
        
        # Setup image directory
        self.images_dir = os.path.join("assets", "product_images")
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Build UI sections
        self._create_header(main_container)
        self._create_toolbar(main_container)
        self._create_views(main_container)
        
        self.refresh_table()
        self.refresh_grid()
    
    # ==================== UI BUILDERS ====================
    
    def _create_header(self, parent):
        """Header with title"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 20))
        title = "Inventory" if self.is_admin else "Products"
        ctk.CTkLabel(frame, text=title, font=ModernTheme.get_title_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w")
    
    def _create_toolbar(self, parent):
        """Toolbar with all controls"""
        card = ModernTheme.create_modern_card(parent)
        card.pack(fill="x", pady=(0, 20))
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=12)
        
        # Row 1: Search & View toggle
        row1 = ctk.CTkFrame(content, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))
        
        # Search
        search_f = ctk.CTkFrame(row1, fg_color="transparent")
        search_f.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        self.search_entry = ctk.CTkEntry(search_f, placeholder_text="Search products...", height=40,
                                          fg_color=ModernTheme.SURFACE, border_color=ModernTheme.BORDER,
                                          border_width=1, text_color=ModernTheme.TEXT_PRIMARY)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        self.view_var = tk.StringVar(value="grid")
        ctk.CTkRadioButton(row1, text="Table", variable=self.view_var, value="table",
                          command=self.switch_view, text_color=ModernTheme.TEXT_PRIMARY).pack(side="left", padx=8)
        ctk.CTkRadioButton(row1, text="Grid", variable=self.view_var, value="grid",
                          command=self.switch_view, text_color=ModernTheme.TEXT_PRIMARY).pack(side="left", padx=8)
        
        self.sort_combo = ctk.CTkOptionMenu(row1, values=["None", "Price ↓", "Price ↑", "Rating ↓"],
                                            command=self.on_sort, fg_color=ModernTheme.SURFACE,
                                            button_color=ModernTheme.PRIMARY, text_color=ModernTheme.TEXT_PRIMARY)
        self.sort_combo.set("Sort")
        self.sort_combo.pack(side="left", padx=(10, 0))
        
        # Row 2: Filters
        row2 = ctk.CTkFrame(content, fg_color="transparent")
        row2.pack(fill="x", pady=(8, 0))
        
        ctk.CTkLabel(row2, text="Filters:", text_color=ModernTheme.TEXT_PRIMARY).pack(side="left", padx=(0, 8))
        
        self.cat_filter_combo = ctk.CTkOptionMenu(row2, values=["All"] + [c.name for c in self.app.categories],
                                                  command=self.on_filter, fg_color=ModernTheme.SURFACE,
                                                  button_color=ModernTheme.PRIMARY, text_color=ModernTheme.TEXT_PRIMARY, width=130)
        self.cat_filter_combo.set("All")
        self.cat_filter_combo.pack(side="left", padx=3)
        
        self.stock_filter_combo = ctk.CTkOptionMenu(row2, values=["All Stock", "In Stock", "Low Stock", "Out"],
                                                    command=self.on_filter, fg_color=ModernTheme.SURFACE,
                                                    button_color=ModernTheme.PRIMARY, text_color=ModernTheme.TEXT_PRIMARY, width=120)
        self.stock_filter_combo.set("All Stock")
        self.stock_filter_combo.pack(side="left", padx=3)
        
        self.rating_filter_combo = ctk.CTkOptionMenu(row2, values=["All Ratings", "4★+", "3★+", "Unrated"],
                                                     command=self.on_filter, fg_color=ModernTheme.SURFACE,
                                                     button_color=ModernTheme.PRIMARY, text_color=ModernTheme.TEXT_PRIMARY, width=120)
        self.rating_filter_combo.set("All Ratings")
        self.rating_filter_combo.pack(side="left", padx=3)
        
        ModernTheme.create_modern_button(row2, "Clear", command=self.clear_filters,
                                        color="secondary", height=40, width=90).pack(side="left", padx=(8, 0))
        
        # Row 3: Action buttons
        if self.is_admin:
            # Admin buttons
            self.add_btn = ModernTheme.create_modern_button(row2, "Add Product", command=self.add_product,
                                                             color="success", height=40, width=120)
            self.add_btn.pack(side="left", padx=5)
            
            self.edit_btn = ModernTheme.create_modern_button(row2, "Edit", command=self.edit_product,
                                                              color="primary", height=40, width=100)
            self.edit_btn.pack(side="left", padx=5)
            self.edit_btn.configure(state="disabled")
            
            self.del_btn = ModernTheme.create_modern_button(row2, "Delete", command=self.delete_product,
                                                             color="danger", height=40, width=100)
            self.del_btn.pack(side="left", padx=5)
            self.del_btn.configure(state="disabled")
        else:
            # Customer buttons
            self.add_cart_btn = ModernTheme.create_modern_button(row2, "Add to Cart", command=self.add_to_cart,
                                                                 color="success", height=40, width=140)
            self.add_cart_btn.pack(side="right", padx=(5, 0))
            self.add_cart_btn.configure(state="disabled")
            
            self.rate_btn = ModernTheme.create_modern_button(row2, "Rate", command=self.rate_product,
                                                             color="primary", height=40, width=90)
            self.rate_btn.pack(side="right", padx=5)
            self.rate_btn.configure(state="disabled")
            
            self.wish_btn = ctk.CTkButton(row2, text="Wishlist", height=40, width=120,
                                          fg_color="transparent", border_width=2, border_color=ModernTheme.PRIMARY,
                                          text_color=ModernTheme.PRIMARY, hover_color=ModernTheme.SURFACE_HOVER,
                                          command=self.toggle_wishlist, font=ModernTheme.get_label_font())
            self.wish_btn.pack(side="right", padx=5)
            self.wish_btn.configure(state="disabled")
    
    def _create_views(self, parent):
        """Create both table and grid views"""
        self.content_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)
        
        # Table View
        self._create_table_view()
        
        # Grid View
        self._create_grid_view()
        
        self.switch_view()
    
    def _create_table_view(self):
        """Create table view container"""
        # Centralized styling is already initialized in app.py via ModernTheme.setup_appearance()
        
        self.table_frame_container = ModernTheme.create_modern_card(self.content_container)
        
        cols = ("ID", "Name", "Price", "Category", "Stock", "Rating")
        self.tree = ttk.Treeview(self.table_frame_container, columns=cols, show="headings", height=16)
        
        # Configure alternating row colors
        self.tree.tag_configure('oddrow', background=ModernTheme.BG_SECONDARY)
        self.tree.tag_configure('evenrow', background=ModernTheme.SURFACE)
        
        for col in cols:
            self.tree.heading(col, text=col)
            width = 160 if col == "Name" else 140 if col == "Category" else 100
            self.tree.column(col, width=width, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
    
    def _create_grid_view(self):
        """Create grid view container"""
        self.grid_frame_container = ModernTheme.create_modern_card(self.content_container)
        self.grid_scroll = ctk.CTkScrollableFrame(self.grid_frame_container, fg_color="transparent")
        self.grid_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.grid_container = ctk.CTkFrame(self.grid_scroll, fg_color="transparent")
        self.grid_container.pack(fill="x", padx=5, pady=5)
        
    # ==================== VIEW SWITCHING ====================
    
    def switch_view(self):
        """Toggle between table and grid view"""
        if self.view_var.get() == "table":
            self.table_frame_container.pack(fill="both", expand=True, padx=8, pady=8)
            self.grid_frame_container.pack_forget()
        else:
            self.table_frame_container.pack_forget()
            self.grid_frame_container.pack(fill="both", expand=True, padx=8, pady=8)
            self.refresh_grid()
    
    # ==================== DATA LOADING ====================
    
    def refresh_table(self):
        """Refresh table with filtered data"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Apply filters
        data = self._get_filtered_products()
        self.filtered_products = data
        
        # Populate table
        for i, product in enumerate(data):
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            
            values = (product.get_product_id(), product.get_name(),
                     f"${product.get_price():.2f}", product.get_category(),
                     product.get_stock(), f"{product.get_average_rating():.1f}")
            self.tree.insert("", tk.END, values=values, tags=(tag,))
        
        if self.view_var.get() == "grid":
            self.refresh_grid()
    
    def refresh_grid(self):
        """Refresh grid view (Fixed 2-columns)"""
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        
        if not self.filtered_products:
            ctk.CTkLabel(self.grid_container, text="No products found",
                        text_color=ModernTheme.TEXT_SECONDARY, font=ModernTheme.get_label_font()).pack(pady=50)
            return
        
        # Fixed 2-column grid
        num_cols = 2
        for i in range(num_cols):
            self.grid_container.grid_columnconfigure(i, weight=1)
            
        for idx, product in enumerate(self.filtered_products):
            row, col = idx // num_cols, idx % num_cols
            self._create_product_card(row, col, product)
    
    def _create_product_card(self, row, col, product):
        """Create a premium product card for grid view"""
        card = ModernTheme.create_modern_card(self.grid_container, corner_radius=16)
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        
        # Upper section for image - FULL WIDTH
        img_frame = ctk.CTkFrame(card, fg_color=ModernTheme.BG_SECONDARY, corner_radius=12, height=180)
        img_frame.pack(fill="x", padx=0, pady=0) # Removed padding for "full" look
        img_frame.pack_propagate(False)
        
        img_path = os.path.join(self.images_dir, f"product_{product.get_product_id()}.jpg")
        
        if os.path.exists(img_path):
            try:
                raw_img = Image.open(img_path)
                # Use ImageOps.fit to fill the 280x180 area
                from PIL import ImageOps
                fit_img = ImageOps.fit(raw_img, (300, 180), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=fit_img, dark_image=fit_img, size=(300, 180))
                img_label = ctk.CTkLabel(img_frame, image=ctk_img, text="")
                img_label.image = ctk_img 
                img_label.pack(fill="both", expand=True)
            except:
                ctk.CTkLabel(img_frame, text="X", font=("Arial", 32)).pack(expand=True)
        else:
            ctk.CTkLabel(img_frame, text="No Image", font=("Arial", 22), text_color=ModernTheme.TEXT_SECONDARY).pack(expand=True)
            
        # Details section
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Category Badge (Small)
        cat_lbl = ctk.CTkLabel(info_frame, text=product.get_category().upper(), 
                              font=ctk.CTkFont(size=9, weight="bold"),
                              fg_color=ModernTheme.BG_SECONDARY, text_color=ModernTheme.PRIMARY,
                              corner_radius=4, padx=6)
        cat_lbl.pack(anchor="w")
        
        # Name
        name_lbl = ctk.CTkLabel(info_frame, text=product.get_name()[:25], 
                               font=ctk.CTkFont(size=15, weight="bold"),
                               text_color=ModernTheme.TEXT_PRIMARY)
        name_lbl.pack(anchor="w", pady=(5, 2))
        
        # Price & Rating Row
        meta_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        meta_row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(meta_row, text=f"${product.get_price():.2f}", 
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=ModernTheme.SUCCESS).pack(side="left")
        
        rating_val = product.get_average_rating()
        star_str = "★" * int(rating_val) + "☆" * (5 - int(rating_val))
        ctk.CTkLabel(meta_row, text=f"{star_str} ({rating_val:.1f})", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=ModernTheme.WARNING).pack(side="right")
        
        # Actions Row
        actions = ctk.CTkFrame(info_frame, fg_color="transparent")
        actions.pack(fill="x", side="bottom", pady=(10, 0))
        
        if self.is_admin:
            # Multi-icon layout for admins
            ModernTheme.create_modern_button(actions, "Edit", height=32, width=60,
                                            command=lambda p=product: self._open_product_form(p)).pack(side="left", padx=2)
            ModernTheme.create_modern_button(actions, "Img", height=32, width=60, color="info",
                                            command=lambda p=product: self._upload_image(p)).pack(side="left", padx=2)
            ModernTheme.create_modern_button(actions, "View", height=32, width=60, color="secondary",
                                            command=lambda p=product: self._view_product_details(p)).pack(side="left", padx=2)
            ModernTheme.create_modern_button(actions, "Del", height=32, width=60, color="danger",
                                            command=lambda p=product: self._delete_from_grid(p)).pack(side="right", padx=2)
        else:
            # Customer Experience
            ModernTheme.create_modern_button(actions, "Add", height=35, color="success", font=ctk.CTkFont(size=12, weight="bold"),
                                            command=lambda p=product: self._add_to_cart_grid(p)).pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            ModernTheme.create_modern_button(actions, "View", height=35, width=60, color="info",
                                            command=lambda p=product: self._view_product_details(p)).pack(side="right")
            
            ModernTheme.create_modern_button(actions, "Wish", height=35, width=60, color="primary",
                                            command=lambda p=product: self._toggle_wishlist_grid(p)).pack(side="right", padx=5)

    def _view_product_details(self, product):
        """Show full product details in a modern popup"""
        detail_win = ctk.CTkToplevel(self)
        detail_win.title(f"Product Details - {product.get_name()}")
        detail_win.geometry("600x700")
        detail_win.configure(fg_color=ModernTheme.BG_PRIMARY)
        detail_win.attributes("-topmost", True)
        
        scroll = ctk.CTkScrollableFrame(detail_win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Larger Image
        img_path = os.path.join(self.images_dir, f"product_{product.get_product_id()}.jpg")
        if os.path.exists(img_path):
            try:
                from PIL import ImageOps
                raw_img = Image.open(img_path)
                fit_img = ImageOps.fit(raw_img, (500, 300), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(500, 300))
                lbl = ctk.CTkLabel(scroll, image=ctk_img, text="")
                lbl.image = ctk_img
                lbl.pack(pady=10)
            except: pass
            
        # Info
        ctk.CTkLabel(scroll, text=product.get_name(), font=ctk.CTkFont(size=24, weight="bold"),
                    text_color=ModernTheme.PRIMARY).pack(anchor="w", pady=(10, 0))
        
        ctk.CTkLabel(scroll, text=f"Category: {product.get_category()}", font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_SECONDARY).pack(anchor="w")
        
        price_f = ctk.CTkFrame(scroll, fg_color="transparent")
        price_f.pack(fill="x", pady=15)
        ctk.CTkLabel(price_f, text=f"${product.get_price():.2f}", font=ctk.CTkFont(size=28, weight="bold"),
                    text_color=ModernTheme.SUCCESS).pack(side="left")
        
        # Details
        ctk.CTkLabel(scroll, text="Description", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5))
        desc = product.get_description() or "No description available for this product."
        ctk.CTkLabel(scroll, text=desc, wraplength=540, justify="left",
                    font=ModernTheme.get_label_font(), text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w")
        
        # Reviews
        ctk.CTkLabel(scroll, text=f"Reviews (⭐ {product.get_average_rating():.1f})", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(20, 10))
        
        reviews = product.get_reviews()
        if not reviews:
            ctk.CTkLabel(scroll, text="No reviews yet.", font=ModernTheme.get_small_font(),
                        text_color=ModernTheme.TEXT_SECONDARY).pack(anchor="w")
        else:
            for r in reviews:
                r_card = ModernTheme.create_modern_card(scroll)
                r_card.pack(fill="x", pady=5)
                ctk.CTkLabel(r_card, text=f"👤 {r.get('user', 'User')} • {'⭐' * r.get('rating', 0)}",
                            font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(5, 0))
                ctk.CTkLabel(r_card, text=r.get('comment', ''), font=ModernTheme.get_small_font(),
                            wraplength=500).pack(anchor="w", padx=10, pady=(0, 5))
                            
        ctk.CTkButton(scroll, text="Close Window", command=detail_win.destroy, 
                      fg_color=ModernTheme.BG_SECONDARY, text_color=ModernTheme.TEXT_PRIMARY).pack(pady=30)
    
    def _get_filtered_products(self):
        """Get products with all filters applied"""
        search_q = self.search_entry.get().lower()
        cat_filter = self.cat_filter_combo.get()
        stock_filter = self.stock_filter_combo.get()
        rating_filter = self.rating_filter_combo.get()
        sort_val = self.sort_combo.get()
        
        # Start with visible products
        data = self.app.current_user.view_products(self.app.products)
        products = [next((p for p in self.app.products if p.get_product_id() == d["ID"]), None) for d in data]
        products = [p for p in products if p]
        
        # Apply search
        if search_q:
            products = [p for p in products if search_q in p.get_name().lower() or search_q in p.get_category().lower()]
        
        # Apply category filter
        if cat_filter != "All":
            products = [p for p in products if p.get_category() == cat_filter]
        
        # Apply stock filter
        if stock_filter == "In Stock":
            products = [p for p in products if p.get_stock() > 0]
        elif stock_filter == "Low Stock":
            products = [p for p in products if 0 < p.get_stock() < 10]
        elif stock_filter == "Out":
            products = [p for p in products if p.get_stock() == 0]
        
        # Apply rating filter
        if rating_filter == "4★+":
            products = [p for p in products if p.get_average_rating() >= 4]
        elif rating_filter == "3★+":
            products = [p for p in products if p.get_average_rating() >= 3]
        elif rating_filter == "Unrated":
            products = [p for p in products if p.get_average_rating() == 0]
        
        # Apply sorting
        if sort_val == "Price ↓":
            products.sort(key=lambda p: p.get_price())
        elif sort_val == "Price ↑":
            products.sort(key=lambda p: p.get_price(), reverse=True)
        elif sort_val == "Rating ↓":
            products.sort(key=lambda p: p.get_average_rating(), reverse=True)
        
        return products
    
    # ==================== EVENT HANDLERS ====================
    
    def on_search(self, event):
        self.refresh_table()
    
    def on_sort(self, choice):
        self.refresh_table()
    
    def on_filter(self, choice):
        self.refresh_table()
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_entry.delete(0, tk.END)
        self.cat_filter_combo.set("All")
        self.stock_filter_combo.set("All Stock")
        self.rating_filter_combo.set("All Ratings")
        self.sort_combo.set("Sort")
        self.refresh_table()
    
    def on_select(self, event):
        """Handle treeview selection"""
        selected = self.tree.selection()
        has_sel = bool(selected)
        if self.is_admin:
            self.edit_btn.configure(state="normal" if has_sel else "disabled")
            self.del_btn.configure(state="normal" if has_sel else "disabled")
        else:
            self.add_cart_btn.configure(state="normal" if has_sel else "disabled")
            self.rate_btn.configure(state="normal" if has_sel else "disabled")
            self.wish_btn.configure(state="normal" if has_sel else "disabled")
    
    # ==================== PRODUCT OPERATIONS ====================
    
    def add_product(self):
        """Add new product"""
        self._open_product_form(None)
    
    def edit_product(self):
        """Edit selected product"""
        selected = self.tree.selection()
        if not selected:
            return
        pid = int(self.tree.item(selected[0])['values'][0])
        product = next((p for p in self.app.products if p.get_product_id() == pid), None)
        if product:
            self._open_product_form(product)
    
    def delete_product(self):
        """Delete selected product"""
        selected = self.tree.selection()
        if not selected:
            return
        if messagebox.askyesno("Confirm", "Delete this product?"):
            pid = int(self.tree.item(selected[0])['values'][0])
            self.app.products = [p for p in self.app.products if p.get_product_id() != pid]
            self.app.data_manager.save_products(self.app.products)
            self.refresh_table()
    
    def _delete_from_grid(self, product):
        """Delete from grid view"""
        if messagebox.askyesno("Confirm", f"Delete '{product.get_name()}'?"):
            self.app.products.remove(product)
            self.app.data_manager.save_products(self.app.products)
            self.refresh_table()
    
    def _upload_image(self, product):
        """Upload image for product"""
        file = filedialog.askopenfile(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if file:
            # Copy to assets directory
            dest = os.path.join(self.images_dir, f"product_{product.get_product_id()}.jpg")
            shutil.copy(file.name, dest)
            messagebox.showinfo("Success", "Image uploaded!")
            self.refresh_table()
    
    def _open_product_form(self, product=None):
        """Open product form dialog"""
        form = ctk.CTkToplevel(self)
        form.title("Edit" if product else "New Product")
        form.geometry("500x600")
        form.configure(fg_color=ModernTheme.BG_PRIMARY)
        form.attributes("-topmost", True)
        
        # Main frame
        main = ctk.CTkFrame(form, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Title
        ctk.CTkLabel(main, text="Product Details", font=ModernTheme.get_title_font(),
                    text_color=ModernTheme.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Card
        card = ModernTheme.create_modern_card(main)
        card.pack(fill="both", expand=True)
        
        cardcontent = ctk.CTkFrame(card, fg_color="transparent")
        cardcontent.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        fields = {}
        defaults = {
            "Name": product.get_name() if product else "",
            "Price": str(product.get_price()) if product else "0",
            "Stock": str(product.get_stock()) if product else "0",
        }
        
        for label, default in defaults.items():
            ctk.CTkLabel(cardcontent, text=label, font=ModernTheme.get_label_font(),
                        text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 5))
            entry = ctk.CTkEntry(cardcontent, width=300, height=40, fg_color=ModernTheme.SURFACE,
                                border_color=ModernTheme.BORDER, border_width=1)
            entry.insert(0, default)
            entry.pack(pady=(0, 15))
            fields[label] = entry
        
        # Category
        ctk.CTkLabel(cardcontent, text="Category", font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 5))
        if self.app.categories:
            cat_var = tk.StringVar(value=product.get_category() if product else self.app.categories[0].name)
            cat_menu = ctk.CTkOptionMenu(cardcontent, variable=cat_var, values=[c.name for c in self.app.categories],
                                        width=300, height=40, fg_color=ModernTheme.SURFACE,
                                        button_color=ModernTheme.PRIMARY, text_color=ModernTheme.TEXT_PRIMARY)
            cat_menu.pack(pady=(0, 20))
        
        # Image selection
        ctk.CTkLabel(cardcontent, text="Product Image", font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(5, 5))
        
        selected_img_path = tk.StringVar(value=product.get_image() if product else "")
        preview_label = ctk.CTkLabel(cardcontent, text="No Image Selected" if not selected_img_path.get() else "Image ready",
                                    font=ModernTheme.get_small_font(), text_color=ModernTheme.TEXT_SECONDARY)
        preview_label.pack(pady=(0, 5))
        
        def pick_image():
            file = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
            if file:
                selected_img_path.set(file)
                preview_label.configure(text="New Image Selected 🖼️", text_color=ModernTheme.SUCCESS)
        
        ctk.CTkButton(cardcontent, text="📂 Pick Image", command=pick_image, width=300, height=35,
                      fg_color=ModernTheme.BG_SECONDARY, text_color=ModernTheme.TEXT_PRIMARY,
                      hover_color=ModernTheme.BG_TERTIARY).pack(pady=(0, 20))

        # Save button
        def save():
            try:
                name = fields["Name"].get().strip()
                price = float(fields["Price"].get())
                stock = int(fields["Stock"].get())
                category = cat_var.get() if self.app.categories else "General"
                
                if not name:
                    messagebox.showwarning("Invalid", "Product Name is required.")
                    return
                
                # Duplicate Name Validation
                for p in self.app.products:
                    # If editing, skip the CURRENT product object
                    if product and p.get_product_id() == product.get_product_id():
                        continue
                        
                    if p.get_name().lower() == name.lower():
                        messagebox.showwarning("Duplicate Name", f"A product with the name '{name}' already exists.")
                        return
                
                if product:
                    product.set_name(name)
                    product.set_price(price)
                    product.set_stock(stock)
                    product.set_category(category)
                    target_p = product
                else:
                    from models.product import Product
                    new_id = max([p.get_product_id() for p in self.app.products], default=0) + 1
                    target_p = Product(new_id, name, price, stock, category, "")
                    self.app.products.append(target_p)
                
                # Handle Image Copying
                if selected_img_path.get() and selected_img_path.get() != target_p.get_image():
                    # Only copy if it's a NEW path (not the already stored one)
                    if os.path.exists(selected_img_path.get()):
                        dest_name = f"product_{target_p.get_product_id()}.jpg"
                        dest_path = os.path.join(self.images_dir, dest_name)
                        shutil.copy(selected_img_path.get(), dest_path)
                        target_p.set_image(dest_path) # Store relative or absolute? Let's store relative-ish
                
                self.app.data_manager.save_products(self.app.products)
                self.refresh_table()
                form.destroy()
                messagebox.showinfo("Success", "Saved!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ModernTheme.create_modern_button(cardcontent, "💾 Save", command=save, color="success", width=300, height=45).pack()
    
    # ==================== CART & WISHLIST ====================
    
    def add_to_cart(self):
        """Add to cart from table view (customer only)"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Select Product", "Select a product first")
            return
        
        product_id = int(self.tree.item(selection[0])["values"][0])
        product = next((p for p in self.app.products if p.get_product_id() == product_id), None)
        if product:
            self._add_to_cart_grid(product)
    
    def _add_to_cart_grid(self, product):
        """Add specific product to cart with quantity dialog"""
        if product.get_stock() == 0:
            messagebox.showwarning("Out of Stock", f"{product.get_name()} is out of stock")
            return
        
        # Quantity dialog
        dialog = ctk.CTkToplevel(self.master)
        dialog.title("Add to Cart")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.iconbitmap("")
        
        ctk.CTkLabel(dialog, text=f"Add '{product.get_name()}' to cart?", 
                    font=ModernTheme.get_subtitle_font()).pack(pady=10)
        
        qty_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        qty_frame.pack(pady=10)
        
        ctk.CTkLabel(qty_frame, text="Quantity:", font=ModernTheme.get_label_font()).pack(side="left", padx=5)
        qty_entry = ctk.CTkEntry(qty_frame, width=50, placeholder_text="1")
        qty_entry.pack(side="left", padx=5)
        qty_entry.insert(0, "1")
        
        def add_item():
            try:
                qty = int(qty_entry.get())
                if qty <= 0:
                    messagebox.showerror("Invalid", "Quantity must be > 0")
                    return
                if qty > product.get_stock():
                    messagebox.showerror("Invalid", f"Max available: {product.get_stock()}")
                    return
                
                success, msg = self.app.cart.add_item(product, qty)
                if success:
                    messagebox.showinfo("Success", f"Added {qty}x {product.get_name()} to cart")
                    dialog.destroy()
                    if self.add_cart_btn:
                        self.add_cart_btn.configure(state="disabled")
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Invalid", "Enter valid quantity")
        
        ModernTheme.create_modern_button(dialog, "✅ Add to Cart", command=add_item, 
                                        color="success", width=250, height=40).pack(pady=10)
    
    def toggle_wishlist(self):
        """Toggle wishlist from table view (customer only)"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Select Product", "Select a product first")
            return
        
        product_id = int(self.tree.item(selection[0])["values"][0])
        product = next((p for p in self.app.products if p.get_product_id() == product_id), None)
        if product:
            self._toggle_wishlist_grid(product)
    
    def _toggle_wishlist_grid(self, product):
        """Toggle product in user's wishlist"""
        if not self.app.current_user:
            messagebox.showerror("Error", "User not logged in")
            return
        
        wishlist = self.app.current_user.wishlist
        product_id = product.get_product_id()
        
        if product_id in wishlist:
            wishlist.remove(product_id)
            action = "Removed"
        else:
            wishlist.append(product_id)
            action = "Added"
            
        # Save updated user list
        all_users = self.app.data_manager.load_users()
        for i, u in enumerate(all_users):
            if u.user_id == self.app.current_user.user_id:
                all_users[i] = self.app.current_user
                break
        self.app.data_manager.save_users(all_users)
        
        messagebox.showinfo(action, f"{action} '{product.get_name()}' from wishlist")
        self.refresh_table()
        self.refresh_grid()
    
    def rate_product(self):
        """Rate product from table view (customer only)"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Select Product", "Select a product first")
            return
        
        product_id = int(self.tree.item(selection[0])["values"][0])
        product = next((p for p in self.app.products if p.get_product_id() == product_id), None)
        if product:
            self._rate_product_grid(product)
    
    def _rate_product_grid(self, product):
        """Open rating dialog for the product"""
        # Create rating dialog
        dialog = ctk.CTkToplevel(self.master)
        dialog.title("Quick Rating")
        dialog.geometry("380x250")
        dialog.resizable(False, False)
        dialog.iconbitmap("")
        dialog.configure(fg_color=ModernTheme.BG_PRIMARY)
        dialog.attributes("-topmost", True)
        
        # Product name
        ctk.CTkLabel(dialog, text=f"Rate '{product.get_name()}'", 
                    font=ModernTheme.get_subtitle_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(pady=(25, 10))
        
        # Prompt
        ctk.CTkLabel(dialog, text="Select stars to submit instantly:", 
                    font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_SECONDARY).pack(pady=(0, 20))
        
        # Star rating frame
        star_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        star_frame.pack(pady=10)
        
        # Submit function
        def submit_rating(stars):
            try:
                # Add rating to product
                user_name = self.app.current_user.name
                product.add_review(user_name, stars, "Auto-submitted rating")
                self.app.data_manager.save_products(self.app.products)
                
                messagebox.showinfo("Success", f"✅ Rated {stars}⭐ - Thank you!")
                dialog.destroy()
                self.refresh_table()
                self.refresh_grid()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save rating: {str(e)}")
        
        # Star buttons (1-5)
        for i in range(1, 6):
            star_btn = ctk.CTkButton(
                star_frame, text="⭐", width=60, height=60,
                font=("Arial", 28),
                fg_color=ModernTheme.SURFACE_HOVER,
                text_color=ModernTheme.TEXT_SECONDARY,
                hover_color=ModernTheme.WARNING,
                command=lambda r=i: submit_rating(r),
                border_width=2,
                border_color=ModernTheme.BORDER
            )
            star_btn.pack(side="left", padx=5)

