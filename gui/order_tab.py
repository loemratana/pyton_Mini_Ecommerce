import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from models.user import Admin
from gui.theme import ModernTheme

class OrderTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Header
        self.header = ctk.CTkLabel(self, text="Order Tracking & History", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(anchor="w", padx=20, pady=(0, 20))

        # Toolbar frame
        self.toolbar = ctk.CTkFrame(self, corner_radius=10)
        self.toolbar.pack(fill="x", padx=10, pady=10)
        
        if isinstance(self.app.current_user, Admin):
            ctk.CTkLabel(self.toolbar, text="Management Actions:").pack(side="left", padx=15, pady=15)
            self.status_combo = ctk.CTkOptionMenu(self.toolbar, values=["Pending", "Shipped", "Delivered", "Cancelled"])
            self.status_combo.set("Change Status")
            self.status_combo.pack(side="left", padx=5, pady=15)
            
            self.upd_btn = ctk.CTkButton(self.toolbar, text="Apply Changes", width=120, command=self.update_status)
            self.upd_btn.pack(side="left", padx=15, pady=15)
        else:
            self.cancel_btn = ctk.CTkButton(self.toolbar, text="Cancel Selected Order", fg_color="#dc3545", hover_color="#c82333", command=self.cancel_order)
            self.cancel_btn.pack(side="left", padx=15, pady=15)

        # Treeview Container
        self.tree_frame = ctk.CTkFrame(self, corner_radius=10)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Centralized styling is already initialized in app.py via ModernTheme.setup_appearance()

        columns = ("Order ID", "Customer" if isinstance(self.app.current_user, Admin) else "Purchase Items", "Total", "Status", "Processing Date")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=15)
        
        # Configure alternating row colors
        self.tree.tag_configure('oddrow', background=ModernTheme.BG_SECONDARY)
        self.tree.tag_configure('evenrow', background=ModernTheme.SURFACE)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Purchase Items":
                self.tree.column(col, width=300)
            else:
                self.tree.column(col, width=120, anchor="center")
                
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.on_double_click)
        
        self.refresh_table()


    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        role = "Admin" if isinstance(self.app.current_user, Admin) else "Customer"
        
        # Sort orders by date (newest first)
        sorted_orders = sorted(self.app.orders, key=lambda x: x.order_date, reverse=True)
        
        for i, o in enumerate(sorted_orders):
            if role == "Customer" and o.customer_name != self.app.current_user.name:
                continue
                
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            summary = o.summary(role)
            if role == "Admin":
                customer = summary["customer"]
                val = (summary["order_id"], customer, f"${summary['total']:.2f}", summary["status"], summary["order_date"])
            else:
                items_str = ", ".join([f"{i['name']} ({i['quantity']})" for i in summary["items"]])
                val = (summary["order_id"], items_str, f"${summary['total']:.2f}", summary["status"], summary["order_date"])
                
            self.tree.insert("", tk.END, values=val, tags=(tag,))

    def update_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select an order to update.")
            return
            
        oid = self.tree.item(selected[0])['values'][0]
        new_status = self.status_combo.get()
        
        if new_status == "Change Status":
            messagebox.showwarning("Input", "Please select a valid status.")
            return
        
        order = next((o for o in self.app.orders if o.order_id == oid), None)
        if order:
            order.status = new_status
            self.app.data_manager.save_orders(self.app.orders)
            self.refresh_table()
            messagebox.showinfo("Success", f"Order {oid} status successfully updated to {new_status}")

    def cancel_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select an order to cancel.")
            return
            
        oid = self.tree.item(selected[0])['values'][0]
        order = next((o for o in self.app.orders if o.order_id == oid), None)
        
        if order:
            if order.status not in ["Pending", "Paid"]:
                messagebox.showerror("Error", f"Cannot cancel order with status: {order.status}")
                return
                
            if messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel order {oid}?"):
                order.status = "Cancelled"
                self.app.data_manager.save_orders(self.app.orders)
                self.refresh_table()
                messagebox.showinfo("Success", "Your order has been cancelled.")

    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected: return
        oid = self.tree.item(selected[0])['values'][0]
        order = next((o for o in self.app.orders if o.order_id == oid), None)
        
        if order:
            win = ctk.CTkToplevel(self)
            win.title(f"Order #{oid} Details")
            win.geometry("500x550")
            win.attributes("-topmost", True)
            
            ctk.CTkLabel(win, text=f"Order Receipt", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
            
            info_frame = ctk.CTkFrame(win, fg_color="transparent")
            info_frame.pack(fill="x", padx=30)
            
            ctk.CTkLabel(info_frame, text=f"Customer: {order.customer_name}", font=ctk.CTkFont(size=14)).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Address: {order.shipping_address if order.shipping_address else 'N/A'}", font=ctk.CTkFont(size=14)).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Date: {order.order_date}", font=ctk.CTkFont(size=14)).pack(anchor="w")

            ctk.CTkLabel(info_frame, text=f"Status: {order.status}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#3B8ED0").pack(anchor="w")
            
            # Item Table with proper styling
            item_frame = ctk.CTkFrame(win)
            item_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            cols = ("Item", "Qty", "Price", "Subtotal")
            tree = ttk.Treeview(item_frame, columns=cols, show="headings", height=8)
            
            # Configure alternating row colors
            tree.tag_configure('oddrow', background=ModernTheme.BG_SECONDARY)
            tree.tag_configure('evenrow', background=ModernTheme.SURFACE)
            
            for c in cols:
                tree.heading(c, text=c)
                tree.column(c, width=100, anchor="center")
            tree.pack(fill="both", expand=True, padx=5, pady=5)
            
            for i, item in enumerate(order.items):
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                tree.insert("", tk.END, values=(item['name'], item['quantity'], f"${item['price']:.2f}", f"${item['price']*item['quantity']:.2f}"), tags=(tag,))
            
            # Footer / Total
            footer = ctk.CTkFrame(win, fg_color="transparent")
            footer.pack(fill="x", padx=30, pady=20)
            
            if order.discount > 0:
                ctk.CTkLabel(footer, text=f"Discount Applied: -${order.discount:.2f}", text_color="#dc3545").pack(anchor="e")
            
            ctk.CTkLabel(footer, text=f"Grand Total: ${order.total:.2f}", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="e")
            
            ctk.CTkButton(win, text="Close", command=win.destroy, width=120).pack(pady=20)

