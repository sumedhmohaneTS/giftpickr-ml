class ProductMetadata:
    def __init__(self, product_id, age=None, gender=None, occasions=None, relationships=None, interests=None):
        self.product_id = product_id
        self.age = age
        self.gender = gender
        self.occasions = occasions or []
        self.relationships = relationships or []
        self.interests = interests or []

    def to_dict(cls):
        return {
            'product_id': cls.product_id,
            'age': cls.age,
            'gender': cls.gender,
            'interests': cls.interests,
            'occasions': cls.occasions,
            'relationships': cls.relationships,
        }

    @staticmethod
    def from_dict(data):
        return ProductMetadata(
            product_id=data.get('product_id'),
            age=data.get('age', []),
            gender=data.get('gender', []),
            interests=data.get('interests', []),
            occasions=data.get('occasions', []),
            relationships=data.get('relationships', []),
        )
