import json
from bson import ObjectId
from flask import Flask
from flask_restful import Api
from controllers.product_metadata_controller import ProductMetadataController
from controllers.recommendation_controller import RecommendationController

app = Flask(__name__)
api = Api(app)

# Register the controllers
product_metadata_controller = ProductMetadataController()
product_metadata_controller.register(api)

recommendation_controller = RecommendationController()
recommendation_controller.register(api)


@app.route('/health')
def health():
    return {'status': 'ok'}


if __name__ == "__main__":
    app.run(debug=True)
