
from flask import jsonify, request
from flask_restful import Resource
from models.product_metadata import ProductMetadata
from services.product_metadata_service import ProductMetadataService
from utils.api_utils import success_response, error_response


class ProductMetadataController(Resource):
    def __init__(self):
        self.product_metadata_service = ProductMetadataService()

    @classmethod
    def register(cls, api, prefix):
        api.add_resource(cls, prefix+'/product-metadata')

    def post(self):

        requestData = request.get_json()

        if requestData['product_id'] is None:
            return error_response("Product Id is null"), 400

        occasions = requestData['occasions']
        relationships = requestData['relationships']
        interests = requestData['interests']

        dbObj = ProductMetadata(requestData['product_id'],
                                requestData['minAge'],
                                requestData['maxAge'],
                                requestData['gender'],
                                requestData.get('occasions', '').split(','),
                                requestData.get(
                                    'relationships', '').split(','),
                                requestData.get('interests', '').split(',')
                                )

        product_metadata = self.product_metadata_service.create(requestData['product_id'],
                                                                dbObj.to_dict())
        response = success_response(
            'Product metadata upserted successfully', product_metadata,)
        return response, 200

    def get(self):
        product_id = int(request.args.get('product_id'))

        product_metadata = self.product_metadata_service.get_product_metadata_by_id(
            product_id)
        response = success_response(
            'Product metadata fetched successfully', product_metadata)
        return response, 200
