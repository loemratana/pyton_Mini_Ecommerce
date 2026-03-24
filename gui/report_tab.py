import customtkinter as ctk
from tkinter import messagebox

class ReportTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Header
        self.header = ctk.CTkLabel(self, text="Business Analytics Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(anchor="w", padx=20, pady=(0, 20))

        # Metrics Row
        self.metrics_container = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_container.pack(fill="x", padx=10, pady=10)
        
        # Revenue Card
        self.rev_card = self._create_metric_card(self.metrics_container, "Total Revenue", "$0.00", "#1f6aa5")
        self.rev_card.pack(side="left", padx=10, expand=True, fill="both")
        
        # Orders Count Card (Total Orders)
        self.orders_card = self._create_metric_card(self.metrics_container, "Total Transactions", "0", "#28a745")
        self.orders_card.pack(side="left", padx=10, expand=True, fill="both")

        # Low Stock Card
        self.stock_card = self._create_metric_card(self.metrics_container, "Stock Alerts", "0", "#dc3545")
        self.stock_card.pack(side="left", padx=10, expand=True, fill="both")
        self.stock_card.bind("<Button-1>", lambda e: self.show_low_stock())

        # Analysis Section
        self.analysis_frame = ctk.CTkFrame(self, corner_radius=15)
        self.analysis_frame.pack(fill="both", expand=True, padx=10, pady=20)
        
        ctk.CTkLabel(self.analysis_frame, text="Interactive Data Visualization", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        btn_frame = ctk.CTkFrame(self.analysis_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.sales_btn = ctk.CTkButton(btn_frame, text="Generate Monthly Sales Chart", 
                                        font=ctk.CTkFont(size=14), height=50, width=250,
                                        command=self.show_sales_chart)
        self.sales_btn.pack(pady=10)

        self.prod_btn = ctk.CTkButton(btn_frame, text="Analyze Top Selling Products", 
                                       font=ctk.CTkFont(size=14), height=50, width=250,
                                       command=self.show_products_chart)
        self.prod_btn.pack(pady=10)

        self.excel_btn = ctk.CTkButton(btn_frame, text="Generate Excel Full Report", 
                                        font=ctk.CTkFont(size=14), height=50, width=250,
                                        fg_color="#28a745", hover_color="#218838",
                                        command=self.export_excel)
        self.excel_btn.pack(pady=10)
        
        self.refresh_data()


    def _create_metric_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, corner_radius=15, height=120, border_width=2, border_color=color)
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
        lbl_value = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color=color)
        lbl_value.pack()
        
        # Store label reference for updates
        if "Revenue" in title: self.rev_val_lbl = lbl_value
        elif "Transactions" in title: self.orders_val_lbl = lbl_value
        elif "Stock" in title: self.stock_val_lbl = lbl_value
            
        return card

    def refresh_data(self):
        # Update Revenue
        revenue = self.app.analytics.get_total_revenue()
        self.rev_val_lbl.configure(text=f"${revenue:,.2f}")
        
        # Update Orders Count
        self.orders_val_lbl.configure(text=str(len(self.app.orders)))
        
        # Update Stock Alerts
        low_stock = self.app.analytics.get_low_stock_products()
        count = len(low_stock) if not low_stock.empty else 0
        self.stock_val_lbl.configure(text=str(count))

    def show_low_stock(self):
        low_stock = self.app.analytics.get_low_stock_products()
        if low_stock.empty:
            messagebox.showinfo("Inventory Alerts", "All products are well stocked!")
            return
            
        msg = "The following products require attention:\n\n"
        for _, row in low_stock.iterrows():
            msg += f"• {row['name']} : {row['stock']} units left\n"
        messagebox.showwarning("Inventory Shortage", msg)

    def show_sales_chart(self):
        try:
            self.app.analytics.plot_monthly_sales()
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate chart: {str(e)}")

    def show_products_chart(self):
        try:
            self.app.analytics.plot_top_products()
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate chart: {str(e)}")

    def export_excel(self):
        # Allow user to choose destination
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="sales_report.xlsx",
            title="Export Business Report"
        )
        
        if not save_path:
            return
            
        success, msg = self.app.analytics.export_to_excel(save_path)
        if success:
            messagebox.showinfo("Export Successful", msg)
        else:
            messagebox.showerror("Export Failed", f"Excel report generation failed: {msg}")

