import customtkinter as ctk
import tkinter as tk
import os
from models.user import Admin, Customer
from models.cart import ShoppingCart
from gui.product_tab import ProductTab
from gui.cart_tab import CartTab
from gui.order_tab import OrderTab
from gui.report_tab import ReportTab
from gui.profile_tab import ProfileTab
from gui.dashboard_tab import DashboardTab
from gui.wishlist_tab import WishlistTab
from gui.category_tab import CategoryTab
from gui.user_tab import UserTab
from gui.theme import ModernTheme





class ECommerceApp:
    def __init__(self, root, data_manager, analytics, current_user, logout_callback):
        self.root = root
        self.root.title("Antigravity - E-Commerce Dashboard")
        self.root.geometry("1300x800")
        self.root.configure(fg_color=ModernTheme.BG_PRIMARY)
        
        self.data_manager = data_manager
        self.analytics = analytics
        self.current_user = current_user
        self.logout_cb = logout_callback

        
        self.products = self.data_manager.load_products()
        self.orders = self.data_manager.load_orders()
        self.categories = self.data_manager.load_categories()
        self.cart = ShoppingCart()

        
        # Appearance sets
        ModernTheme.setup_appearance()
        
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
        except Exception:
            pass

        self._setup_ui()

    def _setup_ui(self):
        # Grid layout - configure columns with proper weights
        self.root.grid_columnconfigure(0, minsize=250, weight=0)  # Sidebar: fixed 250px width
        self.root.grid_columnconfigure(1, weight=1)              # Content: expand to fill
        self.root.grid_rowconfigure(0, weight=1)

        # Modern Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.root, width=250, fg_color=ModernTheme.BG_SECONDARY, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_columnconfigure(0, weight=0)
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        # Logo section with modern styling
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="ew")
        
        self.logo_label = ctk.CTkLabel(logo_frame, text="Mini E-commerce", 
                                       font=ModernTheme.get_title_font(),
                                       text_color=ModernTheme.PRIMARY)
        self.logo_label.pack(anchor="w")
        
        self.sub_logo = ctk.CTkLabel(logo_frame, text="Store Management Dashboard", 
                                     font=ModernTheme.get_small_font(),
                                     text_color=ModernTheme.TEXT_SECONDARY)
        self.sub_logo.pack(anchor="w")

        # Personal User Section
        user_info_frame = ctk.CTkFrame(self.sidebar_frame, fg_color=ModernTheme.BG_TERTIARY, corner_radius=12)
        user_info_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        # Profile Picture (Circle)
        avatar_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent", width=44, height=44)
        avatar_frame.pack(side="left", padx=10, pady=10)
        avatar_frame.pack_propagate(False)

        img_path = self.current_user.profile_image
        if img_path and os.path.exists(img_path):
            try:
                from PIL import Image, ImageOps, ImageDraw
                raw_img = Image.open(img_path).convert("RGBA")
                size = (44, 44)
                raw_img = ImageOps.fit(raw_img, size, Image.Resampling.LANCZOS)
                mask = Image.new('L', (176, 176), 0) # 4x for AA
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 176, 176), fill=255)
                mask = mask.resize(size, Image.Resampling.LANCZOS)
                circular_img = Image.new('RGBA', size, (0, 0, 0, 0))
                circular_img.paste(raw_img, (0, 0), mask=mask)
                ctk_img = ctk.CTkImage(light_image=circular_img, dark_image=circular_img, size=size)
                self.sidebar_avatar = ctk.CTkLabel(avatar_frame, image=ctk_img, text="")
                self.sidebar_avatar.pack()
            except:
                ctk.CTkLabel(avatar_frame, text="", font=("Arial", 24)).pack()
        else:
            ctk.CTkLabel(avatar_frame, text="", font=("Arial", 24)).pack()

        # Name and Role
        text_f = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        text_f.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(text_f, text=self.current_user.name[:15], font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(10, 0))
        role_label = "Administrator" if isinstance(self.current_user, Admin) else "Customer"
        ctk.CTkLabel(text_f, text=role_label, font=ModernTheme.get_small_font(),
                    text_color=ModernTheme.TEXT_TERTIARY).pack(anchor="w", pady=(0, 10))

        # Divider
        divider = ctk.CTkFrame(self.sidebar_frame, height=1, fg_color=ModernTheme.BORDER)
        divider.grid(row=2, column=0, padx=15, pady=15, sticky="ew")
        # Sidebar buttons
        self.nav_buttons = []
        
        current_row = 3
        self.btn_dashboard = self._create_nav_button("Dashboard", 3, self._show_dashboard)
        self.btn_products = self._create_nav_button("Products", 4, self._show_products)
        
        if not isinstance(self.current_user, Admin):
            self.btn_cart = self._create_nav_button("Shopping Cart", 5, self._show_cart)
            self.btn_wishlist = self._create_nav_button("Wishlist", 6, self._show_wishlist)
        
        current_row = 7
        self.btn_orders = self._create_nav_button("Orders", current_row, self._show_orders)
        current_row += 1

        if isinstance(self.current_user, Admin):
            self.btn_reports = self._create_nav_button("Analytics", current_row, self._show_reports)
            current_row += 1
            self.btn_cats = self._create_nav_button("Categories", current_row, self._show_cats)
            current_row += 1
            self.btn_users = self._create_nav_button("Users", current_row, self._show_users)
            current_row += 1

        self.btn_profile = self._create_nav_button("Profile", current_row, self._show_profile)
        current_row += 1

        # Bottom section divider
        bottom_divider = ctk.CTkFrame(self.sidebar_frame, height=1, fg_color=ModernTheme.BORDER)
        bottom_divider.grid(row=current_row, column=0, padx=15, pady=15, sticky="ew")
        current_row += 1

        # Appearance mode switcher
        appearance_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        appearance_frame.grid(row=current_row, column=0, padx=20, pady=5, sticky="ew")
        current_row += 1
        
        self.appearance_mode_label = ctk.CTkLabel(appearance_frame, text="Theme Mode", 
                                                  font=ModernTheme.get_small_font(),
                                                  text_color=ModernTheme.TEXT_SECONDARY)
        self.appearance_mode_label.pack(anchor="w", pady=(0, 5))
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(appearance_frame, values=["Light", "Dark", "System"],
                                                     command=self.change_appearance_mode_event,
                                                     fg_color=ModernTheme.SURFACE,
                                                     button_color=ModernTheme.PRIMARY,
                                                     text_color=ModernTheme.TEXT_PRIMARY)
        self.appearance_mode_menu.pack(fill="x")
        self.appearance_mode_menu.set("Dark")

        # Logout button (Bottom)
        self.logout_btn = ModernTheme.create_modern_button(self.sidebar_frame, "Sign Out", 
                                                           command=self._logout, color="danger", height=45)
        self.logout_btn.grid(row=current_row, column=0, padx=20, pady=(20, 30), sticky="ew")

        # Main content area
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=ModernTheme.BG_PRIMARY)
        self.content_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Initialize tabs as frames
        try:
            self.dashboard_tab = DashboardTab(self.content_frame, self)
            print("✓ Dashboard tab created")
        except Exception as e:
            print(f"✗ Dashboard tab error: {e}")
            
        try:
            self.product_tab = ProductTab(self.content_frame, self)
            print("✓ Product tab created")
        except Exception as e:
            print(f"✗ Product tab error: {e}")
            
        if not isinstance(self.current_user, Admin):
            try:
                self.cart_tab = CartTab(self.content_frame, self)
                print("✓ Cart tab created")
            except Exception as e:
                print(f"✗ Cart tab error: {e}")
            try:
                self.wishlist_tab = WishlistTab(self.content_frame, self)
                print("✓ Wishlist tab created")
            except Exception as e:
                print(f"✗ Wishlist tab error: {e}")
        else:
            try:
                self.cat_tab = CategoryTab(self.content_frame, self)
                print("✓ Category tab created")
            except Exception as e:
                print(f"✗ Category tab error: {e}")
            try:
                self.user_tab = UserTab(self.content_frame, self)
                print("✓ User tab created")
            except Exception as e:
                print(f"✗ User tab error: {e}")
                
        try:
            self.order_tab = OrderTab(self.content_frame, self)
            print("✓ Order tab created")
        except Exception as e:
            print(f"✗ Order tab error: {e}")

        if isinstance(self.current_user, Admin):
            try:
                self.report_tab = ReportTab(self.content_frame, self)
                print("✓ Report tab created")
            except Exception as e:
                print(f"✗ Report tab error: {e}")
                
        try:
            self.profile_tab = ProfileTab(self.content_frame, self)
            print("✓ Profile tab created")
        except Exception as e:
            print(f"✗ Profile tab error: {e}")

        # Default view
        self._show_dashboard()
        
        # Force window update to display content
        self.root.update_idletasks()


    def _create_nav_button(self, text, row, command):
        try:
            btn = ctk.CTkButton(self.sidebar_frame, text=text, corner_radius=10, 
                                height=45, border_spacing=15, 
                                fg_color="transparent", 
                                text_color=ModernTheme.TEXT_SECONDARY, 
                                hover_color=ModernTheme.SURFACE_HOVER,
                                anchor="w", 
                                font=ModernTheme.get_label_font(),
                                command=command)
            btn.grid(row=row, column=0, padx=15, pady=6, sticky="ew")
            self.nav_buttons.append(btn)
            return btn
        except Exception as e:
            print(f"Error creating button '{text}': {e}")
            return None

    def _select_nav(self, button):
        for btn in self.nav_buttons:
            btn.configure(fg_color="transparent", text_color=ModernTheme.TEXT_SECONDARY)
        button.configure(fg_color=ModernTheme.PRIMARY, text_color=ModernTheme.TEXT_PRIMARY)

    def _show_dashboard(self):
        self._select_nav(self.btn_dashboard)
        self._hide_all()
        self.dashboard_tab.grid(row=0, column=0, sticky="nsew")
        self.dashboard_tab.refresh_data()


    def _show_products(self):
        self._select_nav(self.btn_products)
        self._hide_all()
        self.product_tab.grid(row=0, column=0, sticky="nsew")
        self.product_tab.refresh_table()

    def _show_cart(self):
        self._select_nav(self.btn_cart)
        self._hide_all()
        self.cart_tab.grid(row=0, column=0, sticky="nsew")
        self.cart_tab.refresh_table()

    def _show_wishlist(self):
        self._select_nav(self.btn_wishlist)
        self._hide_all()
        self.wishlist_tab.grid(row=0, column=0, sticky="nsew")
        self.wishlist_tab.refresh_table()

    def _show_orders(self):

        self._select_nav(self.btn_orders)
        self._hide_all()
        self.order_tab.grid(row=0, column=0, sticky="nsew")
        self.order_tab.refresh_table()

    def _show_reports(self):
        self._select_nav(self.btn_reports)
        self._hide_all()
        self.report_tab.grid(row=0, column=0, sticky="nsew")
        self.report_tab.refresh_data()

    def _show_cats(self):
        self._select_nav(self.btn_cats)
        self._hide_all()
        self.cat_tab.grid(row=0, column=0, sticky="nsew")
        self.cat_tab.refresh_table()

    def _show_users(self):
        self._select_nav(self.btn_users)
        self._hide_all()
        self.user_tab.grid(row=0, column=0, sticky="nsew")
        self.user_tab.refresh_users()

    def _show_profile(self):


        self._select_nav(self.btn_profile)
        self._hide_all()
        self.profile_tab.grid(row=0, column=0, sticky="nsew")

    def _logout(self):
        import tkinter.messagebox as msg
        if msg.askyesno("Confirm", "Are you sure you want to log out?"):
            self.logout_cb()


    def _hide_all(self):
        """Hides all dynamically created tabs safely"""
        potential_tabs = [
            'dashboard_tab', 'product_tab', 'order_tab', 'profile_tab',
            'cart_tab', 'wishlist_tab', 'cat_tab', 'user_tab', 'report_tab'
        ]
        
        for tab_name in potential_tabs:
            if hasattr(self, tab_name):
                tab = getattr(self, tab_name)
                if tab:
                    tab.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def refresh_tabs(self):
        """Global refresh for all components to ensure data consistency"""
        # Reload fresh data
        self.products = self.data_manager.load_products()
        self.orders = self.data_manager.load_orders()
        
        # Refresh individual views
        self.dashboard_tab.refresh_data()
        self.product_tab.refresh_table()
        self.order_tab.refresh_table()

        if hasattr(self, 'cart_tab'): self.cart_tab.refresh_table()
        if hasattr(self, 'wishlist_tab'): self.wishlist_tab.refresh_table()
        if hasattr(self, 'report_tab'): self.report_tab.refresh_data()


