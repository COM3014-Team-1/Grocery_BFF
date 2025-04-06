from flask import Flask, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView

# Import your handler and other components
from Application.product.getproduct.getproducthandler import ProductHandler
from Application.product.getproduct.getproductdto import ProductDTO, ProductDTOSchema
from Application.product.getproduct.getproductvm import ProductVM

app = Flask(__name__)

# Create Flask-Smorest blueprint
blueprint = Blueprint("products", __name__, url_prefix="/products", description="Product Management")

# Endpoint to get all products with optional search filter
@blueprint.route("")
class ProductListAPI(MethodView):
    @blueprint.arguments(ProductDTOSchema, location="query")  # Validates query parameter 'search'
    def get(self, data):
        """Retrieve product list with optional search filter"""
        search = data.get('search', '')  # Get the search parameter, if provided, otherwise default to ''
        
        # Get all products asynchronously from handler (synchronously here)
        products = ProductHandler.get_all_products(search)  # Call the synchronous function
        
        # If no products found, return a 404 error
        if not products:
            abort(404, message="No products found")
        
        # Return a list of products as JSON
        return jsonify([product.to_dict() for product in products]), 200  # Assuming product has a `to_dict` method

# Endpoint to get a product by ID
@blueprint.route("/<int:product_id>")
class ProductAPI(MethodView):
    def get(self, product_id):
        """Retrieve a product by ID"""
        
        # Get the product by ID from handler (synchronously)
        product = ProductHandler.get_product_by_id(product_id)  # Call the synchronous function
        
        # If product not found, return a 404 error
        if not product:
            abort(404, message=f"Product with id {product_id} not found")
        
        # Return the product as JSON
        return jsonify(product.to_dict()), 200  # Assuming product has a `to_dict` method


# Register blueprint with the Flask app
app.register_blueprint(blueprint)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
