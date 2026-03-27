class Category:
    def __init__(self, cat_id, name, description="", image=""):
        self.cat_id = cat_id
        self.name = name
        self.description = description
        self.image = image

    def get_category_id(self):
        return self.cat_id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
        
    def get_image(self):
        return self.image

    def to_dict(self):
        return {
            "cat_id": self.cat_id,
            "name": self.name,
            "description": self.description,
            "image": self.image
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["cat_id"],
            data["name"],
            data.get("description", ""),
            data.get("image", "")
        )
