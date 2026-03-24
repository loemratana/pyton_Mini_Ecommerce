import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from models.order import Order
import uuid
import os
from gui.theme import ModernTheme


class CartTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=ModernTheme.BG_PRIMARY)
        self.app = app
        
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))
        
        self.header = ctk.CTkLabel(header_frame, text="Your Shopping Cart", 
                                   font=ModernTheme.get_title_font(),
                                   text_color=ModernTheme.TEXT_PRIMARY)
        self.header.pack(anchor="w")

        # Toolbar frame
        self.toolbar_frame = ModernTheme.create_modern_card(main_container)
        self.toolbar_frame.pack(fill="x", padx=0, pady=(0, 20))
        
        toolbar_content = ctk.CTkFrame(self.toolbar_frame, fg_color="transparent")
        toolbar_content.pack(fill="x", padx=20, pady=15)
        
        self.upd_btn = ModernTheme.create_modern_button(toolbar_content, "Update Qty", 
                                                        width=140, command=self.update_qty, 
                                                        color="primary", height=40)
        self.upd_btn.pack(side="left", padx=(0, 10))
        self.upd_btn.configure(state="disabled")
        
        self.rm_btn = ModernTheme.create_modern_button(toolbar_content, "Remove Item", 
                                                       width=140, command=self.remove_item, 
                                                       color="danger", height=40)
        self.rm_btn.pack(side="left", padx=(0, 0))
        self.rm_btn.configure(state="disabled")
        
        # Treeview Container
        self.tree_frame = ModernTheme.create_modern_card(main_container)
        self.tree_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Centralized styling is already initialized in app.py via ModernTheme.setup_appearance()

        columns = ("Product ID", "Name", "Price", "Qty", "Total")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=10)
        
        # Configure alternating row colors
        self.tree.tag_configure('oddrow', background=ModernTheme.BG_SECONDARY)
        self.tree.tag_configure('evenrow', background=ModernTheme.SURFACE)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Checkout section - modern card design
        self.checkout_frame = ModernTheme.create_modern_card(main_container)
        self.checkout_frame.pack(fill="x", padx=0)
        
        checkout_content = ctk.CTkFrame(self.checkout_frame, fg_color="transparent")
        checkout_content.pack(fill="x", padx=25, pady=20)
        
        # Left: Total Summary
        summary_frame = ctk.CTkFrame(checkout_content, fg_color="transparent")
        summary_frame.pack(side="left", anchor="w")
        
        summary_label = ctk.CTkLabel(summary_frame, text="Order Summary",
                                     font=ModernTheme.get_label_font(),
                                     text_color=ModernTheme.TEXT_SECONDARY)
        summary_label.pack(anchor="w", pady=(0, 10))
        
        self.total_lbl = ctk.CTkLabel(summary_frame, text="Total: $0.00",
                                      font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
                                      text_color=ModernTheme.SUCCESS)
        self.total_lbl.pack(anchor="w")
        
        self.items_count_lbl = ctk.CTkLabel(summary_frame, text="0 items in cart",
                                            font=ModernTheme.get_small_font(),
                                            text_color=ModernTheme.TEXT_SECONDARY)
        self.items_count_lbl.pack(anchor="w")

        # Right: Checkout actions
        action_frame = ctk.CTkFrame(checkout_content, fg_color="transparent")
        action_frame.pack(side="right", anchor="e", padx=(20, 0))

        self.check_btn = ModernTheme.create_modern_button(action_frame, "💳 Checkout",
                                                          command=self.checkout,
                                                          color="success", height=40, width=150)
        self.check_btn.pack(side="left")

        self.refresh_table()

    def on_select(self, event):
        selected = self.tree.selection()
        state = "normal" if selected else "disabled"
        self.upd_btn.configure(state=state)
        self.rm_btn.configure(state=state)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        items = self.app.cart.get_items()
        total = 0
        for item in items:
            p = item["product"]
            qty = item["quantity"]
            price = p.get_price() # Using full price now
            total += price * qty
            
            tag = 'oddrow' if item in items[::2] else 'evenrow'
            self.tree.insert("", tk.END, values=(
                p.get_product_id(), p.get_name(), f"${price:.2f}", qty, f"${price*qty:.2f}"
            ), tags=(tag,))
            
        self.total_lbl.configure(text=f"Total Amount: ${total:.2f}")
        self.items_count_lbl.configure(text=f"{len(items)} items in cart")

    def update_qty(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        
        qty_window = ctk.CTkToplevel(self)
        qty_window.title("Update Quantity")
        qty_window.geometry("300x150")
        qty_window.attributes("-topmost", True)
        
        ctk.CTkLabel(qty_window, text="New Quantity:").pack(pady=10)
        qty_entry = ctk.CTkEntry(qty_window)
        qty_entry.pack(pady=5)
        
        def confirm():
            try:
                q = int(qty_entry.get())
                success, msg = self.app.cart.update_quantity(pid, q)
                if success:
                    qty_window.destroy()
                    self.refresh_table()
                    self.app.cart.save_cart()
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number")
                
        ctk.CTkButton(qty_window, text="Apply Update", command=confirm).pack(pady=15)

    def remove_item(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Remove this item from cart?"):
            self.app.cart.remove_item(pid)
            self.refresh_table()
            self.app.cart.save_cart()

    def checkout(self):
        items = self.app.cart.get_items()
        if not items:
            messagebox.showwarning("Empty", "Cart is empty!")
            return
            
        total = self.app.cart.get_total() # Note: cart total might still use get_discounted_price.
        # Actually, let's just re-calculate it or clear it. 
        # But if the user also wants to remove internal discounts, I should update get_total in models/cart.py
        # Launcher Payment Window
        PaymentWindow(self, total, items)

    def complete_checkout(self, total, items, payment_method, address=""):
        # Reduce Stock
        order_items = []
        for item in items:
            p = item["product"]
            qty = item["quantity"]
            p.set_stock(p.get_stock() - qty)
            order_items.append({
                "product_id": p.get_product_id(),
                "name": p.get_name(),
                "price": p.get_price(),
                "quantity": qty
            })
            
        self.app.data_manager.save_products(self.app.products)
        
        # Create Order
        new_order = Order(
            order_id=str(uuid.uuid4())[:8].upper(),
            customer_name=self.app.current_user.name,
            items=order_items,
            total=total,
            status="Paid",
            payment_method=payment_method,
            shipping_address=address
        )


        self.app.orders.append(new_order)
        self.app.data_manager.save_orders(self.app.orders)
        
        self.app.cart.clear()
        self.app.cart.save_cart()
        self.refresh_table()
        
        # Dashboard notification simulation
        msg = f"Order {new_order.order_id} Successful!\n--------------------------\nTotal Paid: ${total:.2f}\nPayment: {payment_method}\nStatus: {new_order.status}"
        messagebox.showinfo("Checkout Complete", msg)
        self.app.refresh_tabs()

class PaymentWindow(ctk.CTkToplevel):
    def __init__(self, cart_tab, total, items):
        self.subtotal = total
        self.shipping_fee = 5.00 # Initial default
        self.grand_total = self.subtotal + self.shipping_fee

        super().__init__(cart_tab)
        self.cart_tab = cart_tab
        self.total = self.grand_total # Using grand_total for payment
        self.items = items

        
        self.title("Secure Payment")
        self.geometry("500x600")
        self.attributes("-topmost", True)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.configure(fg_color=ModernTheme.BG_PRIMARY)
        ctk.CTkLabel(self, text="Checkout: Shipping & Payment", font=ModernTheme.get_title_font(),
                    text_color=ModernTheme.PRIMARY).pack(pady=20)
        
        # Address Section Card
        self.addr_frame = ModernTheme.create_modern_card(self)
        self.addr_frame.pack(padx=20, pady=10, fill="x")
        
        addr_content = ctk.CTkFrame(self.addr_frame, fg_color="transparent")
        addr_content.pack(padx=15, pady=15, fill="x")
        
        ctk.CTkLabel(addr_content, text="Shipping Address:", text_color=ModernTheme.TEXT_PRIMARY,
                    font=ModernTheme.get_label_font()).pack(padx=10, pady=(5, 5), anchor="w")
        self.addr_entry = ctk.CTkEntry(addr_content, placeholder_text="Enter your full street address", width=400,
                                      fg_color=ModernTheme.SURFACE, border_color=ModernTheme.BORDER, border_width=1)
        self.addr_entry.pack(padx=10, pady=(0, 10), fill="x")

        # Shipping Fee Input
        ctk.CTkLabel(addr_content, text="Shipping Fee ($):", text_color=ModernTheme.TEXT_PRIMARY,
                    font=ModernTheme.get_label_font()).pack(padx=10, pady=(5, 5), anchor="w")
        self.ship_entry = ctk.CTkEntry(addr_content, width=150, fg_color=ModernTheme.SURFACE, 
                                      border_color=ModernTheme.BORDER, border_width=1)
        self.ship_entry.insert(0, f"{self.shipping_fee:.2f}")
        self.ship_entry.pack(padx=10, pady=(0, 10), anchor="w")
        self.ship_entry.bind("<KeyRelease>", self.update_total)

        self.payment_var = tk.StringVar(value="Cash")

        # --- Cash Payment Section ---
        self.payment_frame = ModernTheme.create_modern_card(self)
        self.payment_frame.pack(padx=20, pady=10, fill="both", expand=True)

        payment_content = ctk.CTkFrame(self.payment_frame, fg_color="transparent")
        payment_content.pack(padx=15, pady=15, fill="both", expand=True)

        ctk.CTkLabel(payment_content, text="Cash Payment Details", text_color=ModernTheme.TEXT_PRIMARY,
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 10))

        summary_f = ctk.CTkFrame(payment_content, fg_color="transparent")
        summary_f.pack(pady=10)
        
        self.sub_lbl = ctk.CTkLabel(summary_f, text=f"Subtotal: ${self.subtotal:.2f}", text_color=ModernTheme.TEXT_PRIMARY, font=ModernTheme.get_label_font())
        self.sub_lbl.pack(anchor="e")
        self.ship_lbl = ctk.CTkLabel(summary_f, text=f"Shipping: ${self.shipping_fee:.2f}", text_color=ModernTheme.INFO, font=ModernTheme.get_label_font())
        self.ship_lbl.pack(anchor="e")
        self.total_lbl = ctk.CTkLabel(summary_f, text=f"Order Total: ${self.grand_total:.2f}", text_color=ModernTheme.SUCCESS, font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"))
        self.total_lbl.pack(anchor="e", pady=(10, 0))

        ctk.CTkLabel(payment_content, text="Cash Amount Received:").pack(pady=(20, 5))
        self.cash_entry = ctk.CTkEntry(payment_content, placeholder_text="Enter cash given", width=200, height=45, font=("Roboto", 16))
        self.cash_entry.pack(pady=5)
        self.cash_entry.bind("<KeyRelease>", self.update_change)
        
        self.change_lbl = ctk.CTkLabel(payment_content, text="Change: $0.00", font=ctk.CTkFont(size=16, weight="bold"), text_color="#28a745")
        self.change_lbl.pack(pady=10)
        
        ctk.CTkButton(payment_content, text="Complete Cash Sale", fg_color="#28a745", height=45, command=lambda: self.confirm("Cash")).pack(pady=20)
    def update_total(self, event=None):
        try:
            val = self.ship_entry.get()
            self.shipping_fee = float(val) if val else 0.0
            self.grand_total = self.subtotal + self.shipping_fee
            self.total = self.grand_total # Update payment total
            
            self.ship_lbl.configure(text=f"Shipping: ${self.shipping_fee:.2f}")
            self.total_lbl.configure(text=f"Order Total: ${self.grand_total:.2f}")
            self.update_change() # Also update change calculation
        except ValueError:
            pass

    def update_change(self, event=None):
        try:
            received = float(self.cash_entry.get())
            change = received - self.total
            if change >= 0:
                self.change_lbl.configure(text=f"Change: ${change:.2f}")
            else:
                self.change_lbl.configure(text="Insufficient Amount", text_color="#dc3545")
        except ValueError:
            self.change_lbl.configure(text="Invalid Amount", text_color="#dc3545")

    def confirm(self, method):
        address = self.addr_entry.get()
        if not address:
            messagebox.showerror("Error", "Please provide a shipping address.")
            return

        if method == "Cash":
            val = self.cash_entry.get()
            if not val or float(val) < self.total:
                messagebox.showerror("Error", "Please enter sufficient cash amount.")
                return
        
        self.cart_tab.complete_checkout(self.total, self.items, method, address)
        self.destroy()



