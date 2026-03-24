class Product:
    def __init__(self, product_id, name, price, stock, category, description="", discount=0, reviews=None, image=None):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__category = category
        self.__description = description
        self.__discount = discount
        self.__reviews = reviews if reviews else [] # List of dicts: {"user": str, "rating": int, "comment": str}
        self.__image = image # Path to image
    
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

    def get_reviews(self):
        return self.__reviews
    
    def get_image(self):
        return self.__image

    def add_review(self, user_name, rating, comment):
        self.__reviews.append({"user": user_name, "rating": rating, "comment": comment})

    def get_average_rating(self):
        if not self.__reviews:
            return 0.0
        return sum([r['rating'] for r in self.__reviews]) / len(self.__reviews)


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
        
    def set_image(self, image):
        self.__image = image

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "category": self.__category,
            "description": self.__description,
            "discount": self.__discount,
            "reviews": self.__reviews,
            "image": self.__image
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
            data.get("discount", 0),
            data.get("reviews", []),
            data.get("image", None)
        )

