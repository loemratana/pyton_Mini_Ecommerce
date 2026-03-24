import customtkinter as ctk
from models.user import Admin, Customer
from gui.theme import ModernTheme
import tkinter as tk

class DashboardTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=ModernTheme.BG_PRIMARY)
        self.app = app
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        # Main container with padding
        main_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header section
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        welcome_text = f"👋 Welcome, {self.app.current_user.name}!" if not isinstance(self.app.current_user, Admin) else f"👨‍💼 Admin Dashboard"
        self.header = ctk.CTkLabel(header_frame, text=welcome_text, 
                                   font=ModernTheme.get_header_font(),
                                   text_color=ModernTheme.TEXT_PRIMARY)
        self.header.pack(anchor="w")
        
        self.sub_header = ctk.CTkLabel(header_frame, text="📊 Analytics & System Overview", 
                                       font=ModernTheme.get_small_font(),
                                       text_color=ModernTheme.TEXT_SECONDARY)
        self.sub_header.pack(anchor="w", pady=(5, 0))

        # Quick filters
        filter_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 25))
        
        period_label = ctk.CTkLabel(filter_frame, text="📅 Period:",
                                   font=ModernTheme.get_label_font(),
                                   text_color=ModernTheme.TEXT_SECONDARY)
        period_label.pack(side="left", padx=(0, 10))
        
        self.period_menu = ctk.CTkOptionMenu(filter_frame, values=["Today", "This Week", "This Month", "All Time"],
                                             fg_color=ModernTheme.SURFACE,
                                             button_color=ModernTheme.PRIMARY,
                                             text_color=ModernTheme.TEXT_PRIMARY)
        self.period_menu.set("This Month")
        self.period_menu.pack(side="left", padx=(0, 20))
        
        refresh_btn = ModernTheme.create_modern_button(filter_frame, "🔄 Refresh", 
                                                       command=self.refresh_data, color="primary", width=120, height=35)
        refresh_btn.pack(side="right")

        # Main stats grid (4 cards)
        self.stats_grid = ctk.CTkFrame(main_container, fg_color="transparent")
        self.stats_grid.pack(fill="x", pady=(0, 30))
        
        self._setup_stats()

        # Charts/Analytics section
        analytics_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        analytics_frame.pack(fill="both", expand=True, pady=(0, 30))
        
        chart_title = ctk.CTkLabel(analytics_frame, text="📈 Performance Metrics",
                                   font=ModernTheme.get_subtitle_font(),
                                   text_color=ModernTheme.TEXT_PRIMARY)
        chart_title.pack(anchor="w", pady=(0, 15))
        
        # Two-column chart layout
        charts_container = ctk.CTkFrame(analytics_frame, fg_color="transparent")
        charts_container.pack(fill="both", expand=True)
        
        # Left chart (Revenue/Orders trend)
        self.chart1_frame = ModernTheme.create_modern_card(charts_container)
        self.chart1_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        chart1_content = ctk.CTkFrame(self.chart1_frame, fg_color="transparent")
        chart1_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(chart1_content, text="💰 Revenue Trend",
                    font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 10))
        
        self.chart1_label = ctk.CTkLabel(chart1_content, text="[Chart Visualization]",
                                        font=ModernTheme.get_small_font(),
                                        text_color=ModernTheme.TEXT_SECONDARY)
        self.chart1_label.pack(fill="both", expand=True)
        
        # Right chart (Top categories)
        self.chart2_frame = ModernTheme.create_modern_card(charts_container)
        self.chart2_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        chart2_content = ctk.CTkFrame(self.chart2_frame, fg_color="transparent")
        chart2_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(chart2_content, text="🏆 Top Categories",
                    font=ModernTheme.get_label_font(),
                    text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 10))
        
        self.chart2_label = ctk.CTkLabel(chart2_content, text="[Category Data]",
                                        font=ModernTheme.get_small_font(),
                                        text_color=ModernTheme.TEXT_SECONDARY)
        self.chart2_label.pack(fill="both", expand=True)

        # Recent Activity section with better formatting
        self.recent_frame = ModernTheme.create_modern_card(main_container)
        self.recent_frame.pack(fill="both", expand=True)
        
        recent_header = ctk.CTkFrame(self.recent_frame, fg_color="transparent")
        recent_header.pack(fill="x", padx=25, pady=(20, 15))
        
        ctk.CTkLabel(recent_header, text="📈 Recent Activity", 
                     font=ModernTheme.get_subtitle_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w")
        
        self.activity_box = ctk.CTkTextbox(self.recent_frame, 
                                          font=ModernTheme.get_label_font(), 
                                          border_width=0, 
                                          fg_color=ModernTheme.BG_SECONDARY,
                                          text_color=ModernTheme.TEXT_PRIMARY)
        self.activity_box.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        self.activity_box.configure(state="disabled")

        self.refresh_data()

    def _setup_stats(self):
        # Determine which stats to show based on role
        if isinstance(self.app.current_user, Admin):
            stats_data = [
                ("💰 Total Revenue", "$0.0", ModernTheme.SUCCESS, "revenue"),
                ("📦 Total Products", "0", ModernTheme.INFO, "products"),
                ("📋 Active Orders", "0", ModernTheme.WARNING, "orders"),
                ("👥 Total Users", "0", ModernTheme.PRIMARY, "users"),
            ]
        else:
            stats_data = [
                ("🛒 Items in Cart", "0", ModernTheme.PRIMARY, "cart"),
                ("🎁 My Orders", "0", ModernTheme.SUCCESS, "myorders"),
                ("❤️ Wishlist Items", "0", ModernTheme.DANGER, "wishlist"),
                ("💳 Spent This Month", "$0.0", ModernTheme.WARNING, "spent"),
            ]
        
        for title, value, color, key in stats_data:
            self._create_stat_card(title, value, color, key)

    def _create_stat_card(self, title, value, color, key):
        card = ModernTheme.create_modern_card(self.stats_grid)
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        card.pack_forget()  # Will be added to grid
        
        # Store card for grid geometry
        if not hasattr(self, 'cards'):
            self.cards = []
        self.cards.append(card)
        
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(pady=20, padx=20, fill="both")
        
        ctk.CTkLabel(card_content, text=title, 
                     font=ModernTheme.get_label_font(), 
                     text_color=ModernTheme.TEXT_SECONDARY).pack(pady=(0, 10))
        
        val_lbl = ctk.CTkLabel(card_content, text=value, 
                               font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"), 
                               text_color=color)
        val_lbl.pack()
        
        # Store reference for update
        setattr(self, f'val_{key}', val_lbl)

    def refresh_data(self):
        self.app.products = self.app.data_manager.load_products()
        self.app.orders = self.app.data_manager.load_orders()
        users = self.app.data_manager.load_users()
        
        if isinstance(self.app.current_user, Admin):
            revenue = self.app.analytics.get_total_revenue()
            self.val_revenue.configure(text=f"${revenue:,.2f}")
            self.val_products.configure(text=str(len(self.app.products)))
            self.val_orders.configure(text=str(len([o for o in self.app.orders if o.status != 'Cancelled'])))
            self.val_users.configure(text=str(len(users)))
            
            # Update charts
            self.chart1_label.configure(text=f"Total: ${revenue:,.2f}\nOrders: {len(self.app.orders)}")
            top_cats = {}
            for p in self.app.products:
                top_cats[p.get_category()] = top_cats.get(p.get_category(), 0) + 1
            cat_text = "\n".join([f"  • {k}: {v} items" for k, v in sorted(top_cats.items(), key=lambda x: x[1], reverse=True)[:5]]) or "No data"
            self.chart2_label.configure(text=cat_text)
            
            # Activity Log
            log = "📊 Recent System Events:\n" + "─" * 50 + "\n"
            if self.app.orders:
                for o in sorted(self.app.orders, key=lambda x: x.order_date, reverse=True)[:5]:
                    log += f"• [ORDER #{o.order_id}] {o.customer_name} - ${o.total:.2f}\n"
            else:
                log += "No orders yet.\n"
        else:
            cart_items = len(self.app.cart.get_items())
            self.val_cart.configure(text=str(cart_items))
            cust_orders = [o for o in self.app.orders if o.customer_name == self.app.current_user.name]
            self.val_myorders.configure(text=str(len(cust_orders)))
            self.val_wishlist.configure(text=str(len(self.app.current_user.wishlist)))
            
            spent = sum([o.total for o in cust_orders])
            self.val_spent.configure(text=f"${spent:.2f}")
            
            # Update charts
            self.chart1_label.configure(text=f"Cart Items: {cart_items}\nOrders: {len(cust_orders)}\nTotal Spent: ${spent:.2f}")
            order_status = {}
            for o in cust_orders:
                order_status[o.status] = order_status.get(o.status, 0) + 1
            status_text = "\n".join([f"  • {k}: {v}" for k, v in order_status.items()]) or "No orders"
            self.chart2_label.configure(text=status_text)
            
            # Activity Log
            log = "🛍️ Your Purchase Activities:\n" + "─" * 50 + "\n"
            if cust_orders:
                for o in sorted(cust_orders, key=lambda x: x.order_date, reverse=True)[:5]:
                    log += f"• Order #{o.order_id} - {o.status} (${o.total:.2f})\n"
            else:
                log += "No purchases yet. Start shopping!\n"
        
        self.activity_box.configure(state="normal")
        self.activity_box.delete("1.0", "end")
        self.activity_box.insert("1.0", log)
        self.activity_box.configure(state="disabled")
