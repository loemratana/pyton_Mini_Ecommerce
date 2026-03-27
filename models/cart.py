import json

class ShoppingCart:
    def __init__(self):
        # Dictionary to store items as {item_key: {"product": Product_obj, "quantity": int, "size": str, "color": str}}
        # item_key format: "product_id_size_color"
        self.__items = {}

    def add_item(self, product, quantity, size="N/A", color="N/A"):
        """Add item to cart or update quantity if it exists. Cannot exceed stock."""
        item_key = f"{product.get_product_id()}_{size}_{color}"
        
        current_qty = self.__items.get(item_key, {}).get("quantity", 0)
        new_qty = current_qty + quantity
        
        if new_qty > product.get_stock():
            return False, f"Cannot add {quantity} more. Outstanding stock is {product.get_stock()}."
            
        self.__items[item_key] = {
            "product": product,
            "quantity": new_qty,
            "size": size,
            "color": color
        }
        return True, "Added to cart successfully."

    def remove_item(self, item_key):
        if item_key in self.__items:
            del self.__items[item_key]

    def update_quantity(self, item_key, new_quantity):
        if item_key in self.__items:
            product = self.__items[item_key]["product"]
            if new_quantity > product.get_stock():
                return False, "Not enough stock available."
            if new_quantity <= 0:
                self.remove_item(item_key)
            else:
                self.__items[item_key]["quantity"] = new_quantity
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
        # Return items with their keys included for easy access
        res = []
        for key, val in self.__items.items():
            item = val.copy()
            item["key"] = key
            res.append(item)
        return res

    def clear(self):
        self.__items = {}

    def save_cart(self, file_path="cart.json"):
        """Save cart temporarily to cart.json for session persistence"""
        data = []
        for key, item in self.__items.items():
            data.append({
                "product_id": item["product"].get_product_id(),
                "quantity": item["quantity"],
                "size": item["size"],
                "color": item["color"]
            })
        with open(file_path, "w") as f:
            json.dump(data, f)
