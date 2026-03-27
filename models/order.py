from datetime import datetime

class Order:
    def __init__(self, order_id, customer_name, items, total, status="Pending", order_date=None, discount=0.0, payment_method="Cash", shipping_address="", subtotal=0.0, shipping=0.0, tax=0.0):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items # list of dicts: {"product_id": ID, "name": str, "price": float, "quantity": int}
        self.total = total
        self.status = status
        self.order_date = order_date if order_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.discount = discount
        self.payment_method = payment_method
        self.shipping_address = shipping_address
        self.subtotal = subtotal
        self.shipping = shipping
        self.tax = tax

    def summary(self, role="Admin"):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "items": self.items,
            "total": self.total,
            "status": self.status,
            "order_date": self.order_date,
            "payment_method": self.payment_method,
            "shipping_address": self.shipping_address,
            "discount": self.discount,
            "subtotal": self.subtotal,
            "shipping": self.shipping,
            "tax": self.tax
        }

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "items": self.items,
            "total": self.total,
            "status": self.status,
            "order_date": self.order_date,
            "discount": self.discount,
            "payment_method": self.payment_method,
            "shipping_address": self.shipping_address,
            "subtotal": self.subtotal,
            "shipping": self.shipping,
            "tax": self.tax
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
            data.get("discount", 0.0),
            data.get("payment_method", "Cash"),
            data.get("shipping_address", ""),
            data.get("subtotal", 0.0),
            data.get("shipping", 0.0),
            data.get("tax", 0.0)
        )


