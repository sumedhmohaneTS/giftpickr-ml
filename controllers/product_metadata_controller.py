
from flask import jsonify, request
from flask_restful import Resource
from models.product_metadata import ProductMetadata
from services.product_metadata_service import ProductMetadataService
from utils.api_utils import success_response


class ProductMetadataController(Resource):
    def __init__(self):
        self.product_metadata_service = ProductMetadataService()

    @classmethod
    def register(cls, api):
        api.add_resource(cls, '/product-metadata')

    def post(self):

        requestData = request.get_json()

        dbObj = ProductMetadata(requestData['product_id'],
                                requestData['age'],
                                requestData['gender'].split(','),
                                requestData['occasions'].split(','),
                                requestData['relationships'].split(','),
                                requestData['interests'].split(',')
                                )

        product_metadata = self.product_metadata_service.create(
            dbObj.to_dict())
        response = success_response(
            'Product metadata created successfully', product_metadata)
        return response, 200

    def get(self):
        age = request.args.get('age', type=int)
        gender = request.args.get('gender')
        occasion = request.args.get('occasion')
        relationship = request.args.get('relationship')
        interests = request.args.getlist('interests')

        product_metadata = self.product_metadata_service.get_product_metadata(
            age=age, gender=gender, occasion=occasion, relationship=relationship, interests=interests)
        response = success_response(
            'Product metadata created successfully', product_metadata)
        return response, 200
