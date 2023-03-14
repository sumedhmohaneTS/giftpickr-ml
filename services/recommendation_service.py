
from models.product_metadata import ProductMetadata
from models.user_preference import UserPreference
from services.product_metadata_service import ProductMetadataService
from utils.ml_utils import get_recommendationsV2
from typing import List


class RecommendationService:
    def __init__(self, ):
        self.product_metadata_service = ProductMetadataService()

    def get_recommendations(self, age: int = None, gender: str = None, occasion: str = None, relationship: str = None, interests: List[str] = None, minPrice: float = None, maxPrice: float = None) -> List[ProductMetadata]:
        metadata = []
        # self.product_metadata_service.convertToInt()
        # self.product_metadata_service.addBoyfriend()
        if age or gender or occasion or relationship or interests:
            # fetch all product metadata
            metadata = self.product_metadata_service.get_all_for_recommendation(
                age, gender, minPrice, maxPrice)

        # get recommendations based on the product metadata
        user_preference = UserPreference(
            age, gender, occasion, relationship, interests).to_dict()

        recommended_products = get_recommendationsV2(
            user_preference, metadata)

        return recommended_products
