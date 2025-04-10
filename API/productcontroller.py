from flask import Flask, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from config import appsettings

# Import your handler and other components
from Application.product.getproduct.getproducthandler import ProductHandler
from Application.product.getproduct.getproductdto import ProductDTO, ProductDTOSchema
from Application.product.getproduct.getproductvm import ProductVM

app = Flask(__name__)

# Create Flask-Smorest blueprint
blueprint = Blueprint("products", __name__, url_prefix="/products", description="Product Management")

# Load product microservice URL from settings
PROD_MICROSERVICE_URL = appsettings['ProductMicroserviceUrl']

# Create a single instance of ProductHandler (this calls __init__)
product_handler = ProductHandler(PROD_MICROSERVICE_URL)

# Endpoint to get all products with optional search filter
@blueprint.route("")
class ProductListAPI(MethodView):
    @blueprint.arguments(ProductDTOSchema, location="query")
    def get(self, data):
        """Retrieve product list with optional search filter"""
        search = data.get('search', '')
        products = product_handler.get_all_products(search)

        if not products:
            abort(404, message="No products found")

        return jsonify([product.to_dict() for product in products]), 200

# Endpoint to get a product by ID
@blueprint.route("/<int:product_id>")
class ProductAPI(MethodView):
    def get(self, product_id):
        """Retrieve a product by ID"""
        product = product_handler.get_product_by_id(product_id)

        if not product:
            abort(404, message=f"Product with id {product_id} not found")

        return jsonify(product.to_dict()), 200

# Register blueprint with the Flask app
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
