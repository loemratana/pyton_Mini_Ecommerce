import customtkinter as ctk
from models.user import Admin, Customer
from gui.theme import ModernTheme
import tkinter as tk

class DashboardTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=ModernTheme.BG_PRIMARY)
        self.app = app
        
        # Scrollable main content
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        main_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Build sections
        self._create_header(main_container)
        self._create_period_selector(main_container)
        self._create_stats(main_container)
        self._create_analytics(main_container)
        self._create_activity(main_container)
        
        self.refresh_data()
    
    # ==================== UI BUILDERS ====================
    
    def _create_header(self, parent):
        """Create header section"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 25))
        
        is_admin = isinstance(self.app.current_user, Admin)
        welcome = "Admin Dashboard" if is_admin else f"Welcome, {self.app.current_user.name}!"
        
        ctk.CTkLabel(frame, text=welcome, font=ModernTheme.get_header_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(frame, text="Analytics & Overview", font=ModernTheme.get_small_font(),
                    text_color=ModernTheme.TEXT_SECONDARY).pack(anchor="w", pady=(5, 0))
    
    def _create_period_selector(self, parent):
        """Create period filter and refresh button"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(frame, text="Period:", font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_SECONDARY).pack(side="left", padx=(0, 10))
        
        self.period_menu = ctk.CTkOptionMenu(frame, values=["Today", "This Week", "This Month", "All Time"],
                                             fg_color=ModernTheme.SURFACE, button_color=ModernTheme.PRIMARY,
                                             text_color=ModernTheme.TEXT_PRIMARY)
        self.period_menu.set("This Month")
        self.period_menu.pack(side="left", padx=(0, 20))
        
        ModernTheme.create_modern_button(frame, "Refresh", command=self.refresh_data,
                                        color="primary", width=120, height=35).pack(side="right")
    
    def _create_stats(self, parent):
        """Create stat cards section"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 25))
        
        is_admin = isinstance(self.app.current_user, Admin)
        
        if is_admin:
            stats = [
                ("Revenue", "$0.00", ModernTheme.SUCCESS, "revenue"),
                ("Products", "0", ModernTheme.INFO, "products"),
                ("Orders", "0", ModernTheme.WARNING, "orders"),
                ("Users", "0", ModernTheme.PRIMARY, "users"),
            ]
        else:
            stats = [
                ("Cart Items", "0", ModernTheme.PRIMARY, "cart"),
                ("My Orders", "0", ModernTheme.SUCCESS, "myorders"),
                ("Wishlist", "0", ModernTheme.DANGER, "wishlist"),
                ("Spent", "$0.00", ModernTheme.WARNING, "spent"),
            ]
        
        for i, (title, value, color, key) in enumerate(stats):
            self._create_stat_card(frame, i, title, value, color, key)
    
    def _create_stat_card(self, parent, idx, title, value, color, key):
        """Create individual stat card"""
        card = ModernTheme.create_modern_card(parent)
        card.pack(side="left", expand=True, fill="both", padx=(0, 15) if idx < 3 else (0, 0))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text=title, font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_SECONDARY).pack(pady=(0, 8))
        
        value_label = ctk.CTkLabel(content, text=value, font=ctk.CTkFont("Segoe UI", 24, "bold"),
                                  text_color=color)
        value_label.pack()
        
        setattr(self, f"val_{key}", value_label)
    
    def _create_analytics(self, parent):
        """Create analytics section"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, pady=(0, 25))
        
        ctk.CTkLabel(frame, text="Performance Metrics", font=ModernTheme.get_subtitle_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 15))
        
        # Two column layout
        charts = ctk.CTkFrame(frame, fg_color="transparent")
        charts.pack(fill="both", expand=True)
        
        # Left chart
        left_card = ModernTheme.create_modern_card(charts)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        left_content = ctk.CTkFrame(left_card, fg_color="transparent")
        left_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(left_content, text="Revenue Trend", font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 10))
        
        self.chart1_label = ctk.CTkLabel(left_content, text="[Chart Visualization]",
                                        font=ModernTheme.get_small_font(),
                                        text_color=ModernTheme.TEXT_SECONDARY)
        self.chart1_label.pack(fill="both", expand=True)
        
        # Right chart
        right_card = ModernTheme.create_modern_card(charts)
        right_card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        right_content = ctk.CTkFrame(right_card, fg_color="transparent")
        right_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(right_content, text="Top Categories", font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 10))
        
        self.chart2_label = ctk.CTkLabel(right_content, text="[Category Data]",
                                        font=ModernTheme.get_small_font(),
                                        text_color=ModernTheme.TEXT_SECONDARY)
        self.chart2_label.pack(fill="both", expand=True)
    
    def _create_activity(self, parent):
        """Create recent activity section"""
        card = ModernTheme.create_modern_card(parent)
        card.pack(fill="both", expand=True)
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(header, text="Recent Activity", font=ModernTheme.get_subtitle_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w")
        
        self.activity_box = ctk.CTkTextbox(card, font=ModernTheme.get_label_font(),
                                          border_width=0, fg_color=ModernTheme.BG_SECONDARY,
                                          text_color=ModernTheme.TEXT_PRIMARY)
        self.activity_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.activity_box.configure(state="disabled")
    
    # ==================== DATA LOADING ====================
    
    def refresh_data(self):
        """Refresh all dashboard data"""
        self.app.products = self.app.data_manager.load_products()
        self.app.orders = self.app.data_manager.load_orders()
        users = self.app.data_manager.load_users()
        
        is_admin = isinstance(self.app.current_user, Admin)
        
        if is_admin:
            self._update_admin_dashboard(users)
        else:
            self._update_customer_dashboard(users)
    
    def _update_admin_dashboard(self, users):
        revenue = self.app.analytics.get_total_revenue()
        self.val_revenue.configure(text=f"${revenue:,.2f}")
        self.val_products.configure(text=str(len(self.app.products)))
        active_orders = len([o for o in self.app.orders if o.status != 'Cancelled'])
        self.val_orders.configure(text=str(active_orders))
        self.val_users.configure(text=str(len(users)))
        
        self.chart1_label.configure(text=f"Total: ${revenue:,.2f}\nOrders: {active_orders}\nAvg: ${revenue/max(active_orders, 1):.2f}")
        
        top_cats = {}
        for p in self.app.products:
            top_cats[p.get_category()] = top_cats.get(p.get_category(), 0) + 1
        cat_text = "\n".join([f"  • {k}: {v} items" for k, v in sorted(top_cats.items(), key=lambda x: x[1], reverse=True)[:5]]) or "No data"
        self.chart2_label.configure(text=cat_text)
        
        log = "Recent System Events:\n" + "─" * 40 + "\n"
        if self.app.orders:
            for o in sorted(self.app.orders, key=lambda x: x.order_date, reverse=True)[:5]:
                log += f"• #{o.order_id}: {o.customer_name} - ${o.total:.2f}\n"
        else:
            log += "No orders yet.\n"
        
        self.activity_box.configure(state="normal")
        self.activity_box.delete("1.0", "end")
        self.activity_box.insert("1.0", log)
        self.activity_box.configure(state="disabled")
    
    def _update_customer_dashboard(self, users):
        cart_items = len(self.app.cart.get_items())
        self.val_cart.configure(text=str(cart_items))
        
        cust_orders = [o for o in self.app.orders if o.customer_name == self.app.current_user.name]
        self.val_myorders.configure(text=str(len(cust_orders)))
        self.val_wishlist.configure(text=str(len(self.app.current_user.wishlist)))
        
        spent = sum([o.total for o in cust_orders])
        self.val_spent.configure(text=f"${spent:.2f}")
        
        self.chart1_label.configure(text=f"Cart: {cart_items}\nOrders: {len(cust_orders)}\nSpent: ${spent:.2f}")
        
        order_status = {}
        for o in cust_orders:
            order_status[o.status] = order_status.get(o.status, 0) + 1
        status_text = "\n".join([f"  • {k}: {v}" for k, v in order_status.items()]) or "No orders"
        self.chart2_label.configure(text=status_text)
        
        log = "Your Recent Activities:\n" + "─" * 40 + "\n"
        if cust_orders:
            for o in sorted(cust_orders, key=lambda x: x.order_date, reverse=True)[:5]:
                log += f"• Order #{o.order_id} - {o.status} (${o.total:.2f})\n"
        else:
            log += "No purchases yet. Start shopping!\n"
        
        self.activity_box.configure(state="normal")
        self.activity_box.delete("1.0", "end")
        self.activity_box.insert("1.0", log)
        self.activity_box.configure(state="disabled")
