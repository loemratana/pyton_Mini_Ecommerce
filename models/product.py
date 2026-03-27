class Product:
    def __init__(self, product_id, name, price, stock, category, description="", discount=0, reviews=None, images=None, colors=None, sizes=None):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__category = category
        self.__description = description
        self.__discount = discount
        self.__reviews = reviews if reviews else [] # List of dicts
        self.__images = images if images else [] # List of image paths
        self.__colors = colors if colors else [] # List of color strings
        self.__sizes = sizes if sizes else [] # List of size strings
    
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
    
    def get_images(self):
        return self.__images
        
    def get_image(self):
        # Return first image for backward compatibility
        return self.__images[0] if self.__images else None

    def get_colors(self):
        return self.__colors
        
    def get_sizes(self):
        return self.__sizes

    def get_average_rating(self):
        if not self.__reviews:
            return 0.0
        return sum([r['rating'] for r in self.__reviews]) / len(self.__reviews)

    def add_review(self, review):
        self.__reviews.append(review)

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
        
    def set_images(self, images):
        self.__images = images

    def set_colors(self, colors):
        self.__colors = colors
        
    def set_sizes(self, sizes):
        self.__sizes = sizes

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
            "images": self.__images,
            "colors": self.__colors,
            "sizes": self.__sizes
        }

    @classmethod
    def from_dict(cls, data):
        # Handle transformation from old 'image' field to 'images' list
        images = data.get("images", [])
        if "image" in data and data["image"] and not images:
            images = [data["image"]]
            
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data.get("stock", 0),
            data.get("category", ""),
            data.get("description", ""),
            data.get("discount", 0),
            data.get("reviews", []),
            images,
            data.get("colors", []),
            data.get("sizes", [])
        )

