import tkinter as tk
from tkinter import ttk, messagebox

class ReportTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self, text="Admin Dashboard Reports", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.metrics_frame = ttk.Frame(self)
        self.metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.rev_lbl = ttk.Label(self.metrics_frame, text="Total Revenue: $0.00", font=("Arial", 12))
        self.rev_lbl.pack(side=tk.LEFT, padx=20)
        
        self.low_stock_btn = ttk.Button(self.metrics_frame, text="View Low Stock Alerts", command=self.show_low_stock)
        self.low_stock_btn.pack(side=tk.RIGHT, padx=20)

        # Charts section
        charts_frame = ttk.Frame(self)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(charts_frame, text="Show Monthly Sales Chart", command=self.show_sales_chart).pack(pady=5)
        ttk.Button(charts_frame, text="Show Top Products Chart", command=self.show_products_chart).pack(pady=5)
        
        self.refresh_data()

    def refresh_data(self):
        revenue = self.app.analytics.get_total_revenue()
        self.rev_lbl.configure(text=f"Total Revenue: ${revenue:.2f}")

    def show_low_stock(self):
        low_stock = self.app.analytics.get_low_stock_products()
        if low_stock.empty:
            messagebox.showinfo("Alerts", "No low stock products.")
            return
            
        msg = "Low Stock Alerts:\n\n"
        for _, row in low_stock.iterrows():
            msg += f"- {row['name']} (ID: {row['product_id']}): {row['stock']} remaining\n"
        messagebox.showwarning("Low Stock Alerts", msg)

    def show_sales_chart(self):
        self.app.analytics.plot_monthly_sales()

    def show_products_chart(self):
        self.app.analytics.plot_top_products()
