class ProductMetadata:
    def __init__(self, product_id, min_age=None, max_age=None, gender=None, occasions=None, relationships=None, interests=None):
        self.product_id = product_id
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender
        self.occasions = occasions or []
        self.relationships = relationships or []
        self.interests = interests or []
        self.score = 1

    def to_dict(cls):
        return {
            'product_id': cls.product_id,
            'min_age': cls.min_age,
            'max_age': cls.max_age,
            'gender': cls.gender,
            'interests': cls.interests,
            'occasions': cls.occasions,
            'relationships': cls.relationships,
            'score': 1,
        }

    @staticmethod
    def from_dict(data):
        return ProductMetadata(
            product_id=data.get('product_id'),
            min_age=data.get('min_age'),
            max_age=data.get('max_age'),
            gender=data.get('gender'),
            interests=data.get('interests', []),
            occasions=data.get('occasions', []),
            relationships=data.get('relationships', []),
            score=data.get('score', 1),
        )
