import tkinter as tk
from tkinter import ttk, messagebox
from models.user import Admin

class OrderTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        if isinstance(self.app.current_user, Admin):
            ttk.Label(self.toolbar, text="Update Status:").pack(side=tk.LEFT, padx=5)
            self.status_combo = ttk.Combobox(self.toolbar, values=["Pending", "Shipped", "Delivered", "Cancelled"], state="readonly")
            self.status_combo.pack(side=tk.LEFT, padx=5)
            ttk.Button(self.toolbar, text="Update", command=self.update_status).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Button(self.toolbar, text="Cancel Order", command=self.cancel_order).pack(side=tk.LEFT, padx=5)

        columns = ("Order ID", "Customer" if isinstance(self.app.current_user, Admin) else "Items", "Total", "Status", "Date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        role = "Admin" if isinstance(self.app.current_user, Admin) else "Customer"
        
        for o in self.app.orders:
            if role == "Customer" and o.customer_name != self.app.current_user.name:
                continue
                
            summary = o.summary(role)
            if role == "Admin":
                customer = summary["customer"]
                val = (summary["order_id"], customer, f"${summary['total']:.2f}", summary["status"], summary["order_date"])
            else:
                items_str = ", ".join([f"{i['name']}x{i['quantity']}" for i in summary["items"]])
                val = (summary["order_id"], items_str, f"${summary['total']:.2f}", summary["status"], summary["order_date"])
                
            self.tree.insert("", tk.END, values=val)

    def update_status(self):
        selected = self.tree.selection()
        if not selected: return
        oid = self.tree.item(selected[0])['values'][0]
        
        new_status = self.status_combo.get()
        if not new_status: return
        
        order = next((o for o in self.app.orders if o.order_id == oid), None)
        if order:
            order.status = new_status
            self.app.data_manager.save_orders(self.app.orders)
            self.refresh_table()
            messagebox.showinfo("Success", f"Order {oid} status updated to {new_status}")

    def cancel_order(self):
        selected = self.tree.selection()
        if not selected: return
        oid = self.tree.item(selected[0])['values'][0]
        
        order = next((o for o in self.app.orders if o.order_id == oid), None)
        if order:
            if order.status != "Pending":
                messagebox.showerror("Error", "Can only cancel pending orders.")
                return
            order.status = "Cancelled"
            self.app.data_manager.save_orders(self.app.orders)
            self.refresh_table()
            messagebox.showinfo("Success", "Order cancelled.")
