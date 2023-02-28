from flask import Blueprint, jsonify
from app.services.product_metadata_service import ProductMetadataService

product_metadata_controller = Blueprint('product_metadata_controller', __name__)

@product_metadata_controller.route('/product-metadata')
def get_product_metadata():
    age = request.args.get('age', type=int)
    gender = request.args.get('gender')
    occasion = request.args.get('occasion')
    relationship = request.args.get('relationship')
    interests = request.args.getlist('interests')

    product_metadata = ProductMetadataService.get_product_metadata(age=age, gender=gender, occasion=occasion, relationship=relationship, interests=interests)
    return jsonify(product_metadata)

def register_routes(app):
    app.register_blueprint(product_metadata_controller, url_prefix='/product-metadata')