class Product:
    def __init__(self, product_id, name, price, stock, category, description="", discount=0):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__category = category
        self.__description = description
        self.__discount = discount

    # Getters
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_category(self):
        return self.__category

    def get_description(self):
        return self.__description

    def get_discount(self):
        return self.__discount
        
    def get_discounted_price(self):
        if self.__discount > 0:
            return self.__price * (1 - self.__discount / 100.0)
        return self.__price

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_stock(self, stock):
        self.__stock = stock

    def set_category(self, category):
        self.__category = category

    def set_description(self, description):
        self.__description = description

    def set_discount(self, discount):
        self.__discount = discount

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "category": self.__category,
            "description": self.__description,
            "discount": self.__discount
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data.get("stock", 0),
            data.get("category", ""),
            data.get("description", ""),
            data.get("discount", 0)
        )
