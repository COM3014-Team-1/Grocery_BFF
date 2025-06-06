from flask import Flask, jsonify, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from config import appsettings
from Application.product.getproduct.getproducthandler import ProductHandler
from Application.product.getproduct.getproductdto import ProductDTO, ProductDTOSchema
from Application.product.getproduct.getproductvm import ProductVM
from Application.product.getproduct.getproductbycategoryhandler import GetProductByCategoryHandler

app = Flask(__name__)
blueprint = Blueprint("products", __name__, url_prefix="/products", description="Product Management")

PROD_MICROSERVICE_URL = appsettings['ProductMicroserviceUrl']
product_handler = ProductHandler(PROD_MICROSERVICE_URL)
prod_by_category_handler = GetProductByCategoryHandler()


@blueprint.route("")
class ProductListAPI(MethodView):
    @blueprint.arguments(ProductDTOSchema, location="query")
    def get(self, data):
        """Retrieve product list with optional search filter"""
        try:
            search = data.get("search", "")
            products = product_handler.get_all_products(search)

            if not products:
                abort(404, message="No products found")

            return jsonify([product.to_dict() for product in products]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@blueprint.route("/<string:product_id>")
class GetProductByIdAPI(MethodView):
    def get(self, product_id):
        """Get product by product ID with category name"""
        try:
            product = product_handler.get_product_by_id(product_id)
            return jsonify(product.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@blueprint.route("/by-category/<string:category_id>")
class ProductByCategoryAPI(MethodView):
    def get(self, category_id):
        """Retrieve products by category ID"""
        try:
            products = prod_by_category_handler.get_products_by_category(category_id)

            if not products:
                abort(404, message="No products found in this category")

            return jsonify([p.to_dict() for p in products]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
