from database.mongo_db import get_mongo_client

class ProductMetadataRepository:
    def __init__(self):
        self.client = get_mongo_client()
        self.db = self.client["mydatabase"]
        self.collection = self.db["ProductMetadata"]

    def find_by_product_id(self, product_id):
        product_metadata = self.collection.find_one({"product_id": product_id})
        return product_metadata

    def create(self, product_metadata):
        result = self.collection.insert_one(product_metadata)
        return result

    def update(self, product_id, product_metadata):
        result = self.collection.update_one({"product_id": product_id}, {"$set": product_metadata})
        return result

    def delete(self, product_id):
        result = self.collection.delete_one({"product_id": product_id})
        return result

    @staticmethod
    def get_product_metadata(age=None, gender=None, occasion=None, relationship=None, interests=None):
        query = {}
        if age:
            query['age'] = age
        if gender:
            query['gender'] = gender
        if occasion:
            query['occasion'] = occasion
        if relationship:
            query['relationship'] = relationship
        if interests:
            query['interests'] = {'$in': interests}
        return list(self.collection.find(query, {'_id': False}))
