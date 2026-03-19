import tkinter as tk
from tkinter import ttk, messagebox
from models.order import Order
import uuid

class CartTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.upd_btn = ttk.Button(self.toolbar_frame, text="Update Qty", command=self.update_qty, state="disabled")
        self.upd_btn.pack(side=tk.LEFT, padx=5)
        
        self.rm_btn = ttk.Button(self.toolbar_frame, text="Remove", command=self.remove_item, state="disabled")
        self.rm_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ("Product ID", "Name", "Price", "Qty", "Total")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Checkout section
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.total_lbl = ttk.Label(self.bottom_frame, text="Total: $0.00", font=("Arial", 14, "bold"))
        self.total_lbl.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.bottom_frame, text="Coupon:").pack(side=tk.LEFT, padx=(20, 5))
        self.coupon_var = tk.StringVar()
        ttk.Entry(self.bottom_frame, textvariable=self.coupon_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.bottom_frame, text="Checkout", command=self.checkout).pack(side=tk.RIGHT, padx=5)
        
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
        for item in items:
            p = item["product"]
            qty = item["quantity"]
            price = p.get_discounted_price()
            self.tree.insert("", tk.END, values=(
                p.get_product_id(), p.get_name(), f"${price:.2f}", qty, f"${price*qty:.2f}"
            ))
            
        total = self.app.cart.get_total()
        self.total_lbl.configure(text=f"Total: ${total:.2f}")

    def update_qty(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        
        qty_window = tk.Toplevel(self)
        qty_window.title("Update Quantity")
        qty_var = tk.IntVar()
        ttk.Entry(qty_window, textvariable=qty_var).pack(padx=5, pady=5)
        
        def confirm():
            success, msg = self.app.cart.update_quantity(pid, qty_var.get())
            if success:
                qty_window.destroy()
                self.refresh_table()
                self.app.cart.save_cart()
            else:
                messagebox.showerror("Error", msg)
                
        ttk.Button(qty_window, text="Update", command=confirm).pack(pady=5)

    def remove_item(self):
        selected = self.tree.selection()
        if not selected: return
        pid = self.tree.item(selected[0])['values'][0]
        self.app.cart.remove_item(pid)
        self.refresh_table()
        self.app.cart.save_cart()

    def checkout(self):
        items = self.app.cart.get_items()
        if not items:
            messagebox.showwarning("Empty", "Cart is empty!")
            return
            
        total = self.app.cart.get_total()
        discount = 0
        if self.coupon_var.get().lower() == "save10":
            discount = total * 0.10
            total -= discount
            messagebox.showinfo("Coupon", "10% Discount applied!")
            
        # Reduce Stock
        order_items = []
        for item in items:
            p = item["product"]
            qty = item["quantity"]
            p.set_stock(p.get_stock() - qty)
            order_items.append({
                "product_id": p.get_product_id(),
                "name": p.get_name(),
                "price": p.get_discounted_price(),
                "quantity": qty
            })
            
        self.app.data_manager.save_products(self.app.products)
        
        # Create Order
        new_order = Order(
            order_id=str(uuid.uuid4())[:8],
            customer_name=self.app.current_user.name,
            items=order_items,
            total=total,
            status="Pending",
            discount=discount
        )
        self.app.orders.append(new_order)
        self.app.data_manager.save_orders(self.app.orders)
        
        self.app.cart.clear()
        self.app.cart.save_cart()
        self.refresh_table()
        self.coupon_var.set("")
        
        # Email Simulation
        msg = f"Order {new_order.order_id} Confirmed!\nTotal: ${total:.2f}\nItems: {len(order_items)}"
        print("--- EMAIL SIMULATION ---")
        print(msg)
        print("------------------------")
        messagebox.showinfo("Order Placed", msg)
        self.app.refresh_tabs()
