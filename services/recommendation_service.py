
from models.product_metadata import ProductMetadata
from services.product_metadata_service import ProductMetadataService
from utils.ml_utils import get_recommendations
from typing import List


class RecommendationService:
    def __init__(self, ):
        self.product_metadata_service = ProductMetadataService()

    @staticmethod
    def get_recommendations(age: int = None, gender: str = None, occasion: str = None, relationship: str = None, interests: List[str] = None) -> List[ProductMetadata]:
        metadata = []
        if age or gender or occasion or relationship or interests:
            # fetch product metadata based on user inputs
            metadata = ProductMetadataService.get_product_metadata(
                age=age, gender=gender, occasion=occasion, relationship=relationship, interests=interests)

        # get recommendations based on the product metadata
        recommended_products = get_recommendations(metadata)

        return recommended_products
