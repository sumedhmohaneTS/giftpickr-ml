from database.mongo_db import get_mongo_client
from repo.product_metadata_repository import ProductMetadataRepository
from app.models.product_metadata import ProductMetadata

class ProductMetadataService:
    def __init__(self):
        self.mongo_client = get_mongo_client()
        self.product_metadata_repository = ProductMetadataRepository(self.mongo_client)

    def get_product_metadata_by_id(self, product_id):
        product_metadata = self.product_metadata_repository.get_product_metadata_by_id(product_id)
        return product_metadata
    
    @staticmethod
    def get_product_metadata(age=None, gender=None, occasion=None, relationship=None, interests=None):
        product_metadata = self.product_metadata_repository.get_product_metadata(age, gender, occasion, relationship, interests)
        return product_metadata

    def create(product_id, age=None, gender=None, occasion=None, relationship=None, interests=None):
        data = ProductMetadata(product_id, age, gender, occasion, relationship, interests)

        product_metadata = self.product_metadata_repository.create(data)
        return product_metadata
