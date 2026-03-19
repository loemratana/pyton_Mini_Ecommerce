from datetime import datetime

class Order:
    def __init__(self, order_id, customer_name, items, total, status="Pending", order_date=None, discount=0.0):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items # list of dicts: {"product_id": ID, "name": str, "price": float, "quantity": int}
        self.total = total
        self.status = status
        self.order_date = order_date if order_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.discount = discount

    def summary(self, role="Admin"):
        if role == "Admin":
            return {
                "order_id": self.order_id,
                "customer": self.customer_name,
                "items": self.items,
                "total": self.total,
                "status": self.status,
                "order_date": self.order_date
            }
        else:
            # Customer summary: item names, quantities, total
            simplified_items = [{"name": item["name"], "quantity": item["quantity"]} for item in self.items]
            return {
                "order_id": self.order_id,
                "items": simplified_items,
                "total": self.total,
                "status": self.status,
                "order_date": self.order_date
            }

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "items": self.items,
            "total": self.total,
            "status": self.status,
            "order_date": self.order_date,
            "discount": self.discount
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["order_id"],
            data["customer_name"],
            data["items"],
            data["total"],
            data.get("status", "Pending"),
            data.get("order_date"),
            data.get("discount", 0.0)
        )
