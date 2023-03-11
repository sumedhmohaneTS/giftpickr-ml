from database.mongo_db import get_mongo_client
from repo.product_metadata_repository import ProductMetadataRepository


class ProductMetadataService:
    def __init__(self):
        self.mongo_client = get_mongo_client()
        self.product_metadata_repository = ProductMetadataRepository()

    def get_product_metadata_by_id(self, product_id):
        product_metadata = self.product_metadata_repository.find_by_product_id(
            product_id)
        return product_metadata

    def create(self, product_id, data):
        product_metadata = self.get_product_metadata_by_id(product_id)
        if product_metadata is not None:
            product_metadata = self.update(product_id, data)
        else:
            product_metadata = self.product_metadata_repository.create(
                data)

        return product_metadata

    def update(self, product_id, data):
        product_metadata = self.product_metadata_repository.update(
            product_id, data)
        return product_metadata

    def get_all(self):
        return self.product_metadata_repository.get_all()

    def get_all_for_recommendation(self, age, gender):
        return self.product_metadata_repository.get_all_for_recommendation(age, gender)

    def convertToInt(self):
        return self.product_metadata_repository.convertToInt()
