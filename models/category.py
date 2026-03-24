class Category:
    def __init__(self, cat_id, name, description=""):
        self.cat_id = cat_id
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "cat_id": self.cat_id,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["cat_id"],
            data["name"],
            data.get("description", "")
        )
