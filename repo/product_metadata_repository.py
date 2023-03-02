from database.mongo_db import get_mongo_client


class ProductMetadataRepository:
    def __init__(self):
        self.client = get_mongo_client()
        self.db = self.client["gift-recommendation-engine"]
        self.collection = self.db["ProductMetadata"]
        self.defaultProjection = {
            '_id': 0,   # Exclude _id field
        }

    def find_by_product_id(self, product_id):
        product_metadata = self.collection.find_one(
            {"product_id": product_id}, self.defaultProjection)
        return product_metadata

    def create(self, product_metadata):
        result = self.collection.insert_one(product_metadata)
        inserted_id = result.inserted_id
        inserted_document = self.collection.find_one(
            {"_id": inserted_id}, self.defaultProjection)
        return inserted_document

    def update(self, product_id, product_metadata):
        result = self.collection.update_one(
            {"product_id": product_id}, {"$set": product_metadata})
        return self.find_by_product_id(product_id)

    def delete(self, product_id):
        result = self.collection.delete_one({"product_id": product_id})
        return result

    def get_all(self):
        products = self.collection.find({}, self.defaultProjection)
        return [product for product in products]

    def get_all_for_recommendation(self, age, gender):
        query = {}
        if gender:
            query['gender'] = {'$in': ['any', gender]}
        if age:
            query['min_age'] = {'$lte': age}
            query['max_age'] = {'$gte': age}
        products = self.collection.find(query, self.defaultProjection)
        return [product for product in products]
