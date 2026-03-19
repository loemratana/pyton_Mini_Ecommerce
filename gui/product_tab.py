import tkinter as tk
from tkinter import ttk, messagebox
from models.user import Admin, Customer

class ProductTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.toolbar_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(self.toolbar_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        ttk.Label(self.toolbar_frame, text="Sort by:").pack(side=tk.LEFT, padx=5)
        self.sort_combo = ttk.Combobox(self.toolbar_frame, values=["None", "Price (Low-High)", "Price (High-Low)"], state="readonly")
        self.sort_combo.current(0)
        self.sort_combo.pack(side=tk.LEFT, padx=5)
        self.sort_combo.bind("<<ComboboxSelected>>", self.on_sort)

        # Buttons based on role
        if isinstance(self.app.current_user, Admin):
            ttk.Button(self.toolbar_frame, text="Add Product", command=self.add_product).pack(side=tk.RIGHT, padx=5)
            self.edit_btn = ttk.Button(self.toolbar_frame, text="Edit", command=self.edit_product, state="disabled")
            self.edit_btn.pack(side=tk.RIGHT, padx=5)
            self.del_btn = ttk.Button(self.toolbar_frame, text="Delete", command=self.delete_product, state="disabled")
            self.del_btn.pack(side=tk.RIGHT, padx=5)
        else:
            self.add_cart_btn = ttk.Button(self.toolbar_frame, text="Add to Cart", command=self.add_to_cart, state="disabled")
            self.add_cart_btn.pack(side=tk.RIGHT, padx=5)

        # Treeview
        columns = ("ID", "Name", "Price", "Category", "Stock") if isinstance(self.app.current_user, Admin) else ("ID", "Name", "Price", "Discounted Price", "Category", "Stock")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        self.refresh_table()

    def on_search(self, event):
        self.refresh_table()
        
    def on_sort(self, event):
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        query = self.search_entry.get().lower()
        sort_val = self.sort_combo.get()
        
        if not self.app.products:
            return
            
        view_data = self.app.current_user.view_products(self.app.products)
        
        if query:
            view_data = [d for d in view_data if query in str(d["Name"]).lower() or query in str(d["Category"]).lower()]
            
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

        for d in view_data:
            if isinstance(self.app.current_user, Admin):
                values = (d["ID"], d["Name"], f"${d['Price']:.2f}", d["Category"], d["Stock"])
            else:
                values = (d["ID"], d["Name"], f"${d['Price']:.2f}", f"${d['Discounted Price']:.2f}", d["Category"], d["Stock"])
            self.tree.insert("", tk.END, values=values)

    def on_select(self, event):
        selected = self.tree.selection()
        if hasattr(self, 'edit_btn'):
            self.edit_btn.configure(state="normal" if selected else "disabled")
        if hasattr(self, 'del_btn'):
            self.del_btn.configure(state="normal" if selected else "disabled")
        if hasattr(self, 'add_cart_btn'):
            self.add_cart_btn.configure(state="normal" if selected else "disabled")

    def _open_product_form(self, product=None):
        form = tk.Toplevel(self)
        form.title("Product Form")
        
        ttk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_var = tk.StringVar(value=product.get_name() if product else "")
        ttk.Entry(form, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        price_var = tk.DoubleVar(value=product.get_price() if product else 0.0)
        ttk.Entry(form, textvariable=price_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form, text="Stock:").grid(row=2, column=0, padx=5, pady=5)
        stock_var = tk.IntVar(value=product.get_stock() if product else 0)
        ttk.Entry(form, textvariable=stock_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form, text="Category:").grid(row=3, column=0, padx=5, pady=5)
        cat_var = tk.StringVar(value=product.get_category() if product else "")
        ttk.Entry(form, textvariable=cat_var).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form, text="Discount %:").grid(row=4, column=0, padx=5, pady=5)
        disc_var = tk.DoubleVar(value=product.get_discount() if product else 0)
        ttk.Entry(form, textvariable=disc_var).grid(row=4, column=1, padx=5, pady=5)

        def save():
            try:
                if product:
                    product.set_name(name_var.get())
                    product.set_price(price_var.get())
                    product.set_stock(stock_var.get())
                    product.set_category(cat_var.get())
                    product.set_discount(disc_var.get())
                else:
                    from models.product import Product
                    new_id = max([p.get_product_id() for p in self.app.products], default=0) + 1
                    new_p = Product(new_id, name_var.get(), price_var.get(), stock_var.get(), cat_var.get(), "", disc_var.get())
                    self.app.products.append(new_p)
                
                self.app.data_manager.save_products(self.app.products)
                self.refresh_table()
                form.destroy()
            except Exception as e:
                messagebox.showerror("Error", "Invalid inputs: " + str(e))

        ttk.Button(form, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=10)

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
        self.app.products = [p for p in self.app.products if p.get_product_id() != pid]
        self.app.data_manager.save_products(self.app.products)
        self.refresh_table()

    def add_to_cart(self):
        selected = self.tree.selection()
        if not selected:
            return
            
        item = self.tree.item(selected[0])
        pid = item['values'][0]
        product = next((p for p in self.app.products if p.get_product_id() == pid), None)
        
        if product:
            qty_window = tk.Toplevel(self)
            qty_window.title("Quantity")
            ttk.Label(qty_window, text="Quantity:").pack(padx=5, pady=5)
            qty_var = tk.IntVar(value=1)
            ttk.Entry(qty_window, textvariable=qty_var).pack(padx=5, pady=5)
            
            def confirm():
                success, msg = self.app.cart.add_item(product, qty_var.get())
                if success:
                    messagebox.showinfo("Success", msg)
                    self.app.cart.save_cart()
                    qty_window.destroy()
                    self.app.refresh_tabs()
                else:
                    messagebox.showerror("Error", msg)
                    
            ttk.Button(qty_window, text="Add", command=confirm).pack(padx=5, pady=5)
