class ProductMetadata:
    def __init__(self, product_id, interests=None, occasions=None, relationships=None):
        self.product_id = product_id
        self.interests = interests or []
        self.occasions = occasions or []
        self.relationships = relationships or []

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'interests': self.interests,
            'occasions': self.occasions,
            'relationships': self.relationships,
        }

    @staticmethod
    def from_dict(data):
        return ProductMetadata(
            product_id=data.get('product_id'),
            interests=data.get('interests', []),
            occasions=data.get('occasions', []),
            relationships=data.get('relationships', []),
        )
