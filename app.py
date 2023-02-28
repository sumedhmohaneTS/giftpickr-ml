from flask import Flask
from app.controllers.product_metadata_controller import product_metadata_controller
from app.controllers.recommendation_controller import recommendation_controller

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(product_metadata_controller, url_prefix='/product-metadata')
app.register_blueprint(recommendation_controller, url_prefix='/recommed')


if __name__ == "__main__":
    app.run(debug=True)
