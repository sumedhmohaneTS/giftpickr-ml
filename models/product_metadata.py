class ProductMetadata:
    def __init__(self, product_id, min_age=None, max_age=None, gender=None, occasions=None, relationships=None, interests=None, no_of_reviews=None, rating=None, price=None):
        self.product_id = product_id
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender or ['any']
        self.occasions = occasions or ['any']
        self.relationships = relationships or ['any']
        self.interests = interests or ['any']
        self.no_of_reviews = no_of_reviews or 0
        self.rating = rating or 0.0
        self.score = 1
        self.price = price or 0

    def to_dict(cls):
        return {
            'product_id': cls.product_id,
            'min_age': cls.min_age,
            'max_age': cls.max_age,
            'gender': cls.gender,
            'interests': cls.interests,
            'occasions': cls.occasions,
            'relationships': cls.relationships,
            'no_of_reviews': cls.no_of_reviews,
            'rating': cls.rating,
            'score': 1,
            'price': cls.price,
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
            no_of_reviews=data.get('no_of_reviews', 0),
            rating=data.get('rating', 0.0),
            score=data.get('score', 1),
            price=data.get('price', 1.0)
        )
