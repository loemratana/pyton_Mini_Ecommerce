import json

class ShoppingCart:
    def __init__(self):
        # Dictionary to store items as {product_id: {"product": Product_obj, "quantity": int}}
        self.__items = {}

    def add_item(self, product, quantity):
        """Add item to cart or update quantity if it exists. Cannot exceed stock."""
        pid = product.get_product_id()
        current_qty = self.__items.get(pid, {}).get("quantity", 0)
        new_qty = current_qty + quantity
        
        if new_qty > product.get_stock():
            return False, f"Cannot add {quantity} more. Outstanding stock is {product.get_stock()}."
            
        self.__items[pid] = {
            "product": product,
            "quantity": new_qty
        }
        return True, "Added to cart successfully."

    def remove_item(self, product_id):
        if product_id in self.__items:
            del self.__items[product_id]

    def update_quantity(self, product_id, new_quantity):
        if product_id in self.__items:
            product = self.__items[product_id]["product"]
            if new_quantity > product.get_stock():
                return False, "Not enough stock available."
            if new_quantity <= 0:
                self.remove_item(product_id)
            else:
                self.__items[product_id]["quantity"] = new_quantity
            return True, "Quantity updated."
        return False, "Item not in cart."

    def get_total(self):
        """Calculate total price"""
        total = 0.0
        for item in self.__items.values():
            product = item["product"]
            qty = item["quantity"]
            total += product.get_price() * qty
        return total

    def get_items(self):
        return list(self.__items.values())

    def clear(self):
        self.__items = {}

    def save_cart(self, file_path="cart.json"):
        """Save cart temporarily to cart.json for session persistence"""
        data = []
        for pid, item in self.__items.items():
            data.append({
                "product_id": pid,
                "quantity": item["quantity"]
            })
        with open(file_path, "w") as f:
            json.dump(data, f)
