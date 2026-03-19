import pandas as pd
import matplotlib.pyplot as plt

class Analytics:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def _get_orders_df(self):
        orders = self.data_manager.load_orders()
        if not orders:
            return pd.DataFrame()
        return pd.DataFrame([o.to_dict() for o in orders])

    def _get_products_df(self):
        products = self.data_manager.load_products()
        if not products:
            return pd.DataFrame()
        return pd.DataFrame([p.to_dict() for p in products])

    def get_total_revenue(self):
        df = self._get_orders_df()
        if df.empty:
            return 0.0
        
        # Consider orders that are not Cancelled
        completed = df[df['status'] != 'Cancelled']
        if completed.empty:
            return 0.0
        return completed['total'].sum()

    def get_top_selling_products(self):
        orders = self.data_manager.load_orders()
        if not orders:
            return pd.DataFrame()
        
        items_list = []
        for o in orders:
            if o.status != 'Cancelled':
                for item in o.items:
                    items_list.append({
                        "product_id": item["product_id"],
                        "name": item["name"],
                        "quantity": item["quantity"]
                    })
        
        if not items_list:
            return pd.DataFrame()

        df_items = pd.DataFrame(items_list)
        top_products = df_items.groupby(['product_id', 'name'])['quantity'].sum().reset_index()
        top_products = top_products.sort_values(by='quantity', ascending=False)
        return top_products

    def get_monthly_sales(self):
        df = self._get_orders_df()
        if df.empty:
            return pd.Series(dtype=float)
        
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['month'] = df['order_date'].dt.to_period('M')
        
        completed = df[df['status'] != 'Cancelled']
        if completed.empty:
            return pd.Series(dtype=float)
            
        monthly_sales = completed.groupby('month')['total'].sum()
        return monthly_sales

    def get_most_active_customers(self):
        df = self._get_orders_df()
        if df.empty:
            return pd.DataFrame()
            
        completed = df[df['status'] != 'Cancelled']
        if completed.empty:
            return pd.DataFrame()
            
        top_customers = completed.groupby('customer_name')['total'].sum().reset_index()
        top_customers = top_customers.sort_values(by='total', ascending=False)
        return top_customers

    def get_low_stock_products(self, threshold=5):
        df = self._get_products_df()
        if df.empty:
            return pd.DataFrame()
            
        low_stock = df[df['stock'] <= threshold]
        return low_stock

    def plot_monthly_sales(self, save_path=None):
        sales = self.get_monthly_sales()
        if sales.empty:
            return False
            
        plt.figure(figsize=(8, 5))
        sales.plot(kind='bar', color='skyblue')
        plt.title('Monthly Sales Revenue')
        plt.xlabel('Month')
        plt.ylabel('Revenue ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return True
        plt.show()

    def plot_top_products(self, save_path=None, top_n=5):
        top_products = self.get_top_selling_products()
        if top_products.empty:
            return False
            
        top_products = top_products.head(top_n)
        
        plt.figure(figsize=(8, 5))
        plt.bar(top_products['name'], top_products['quantity'], color='lightgreen')
        plt.title(f'Top {top_n} Selling Products')
        plt.xlabel('Product')
        plt.ylabel('Quantity Sold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return True
        plt.show()
