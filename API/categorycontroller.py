from flask import Flask, jsonify, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from config import appsettings

from Application.category.getcategory.getcategoryhandler import CategoryHandler
from Application.category.getcategory.categoryvm import CategoryVM

app = Flask(__name__)
blueprint = Blueprint("categories", __name__, url_prefix="/categories", description="Category Management")

# Load Product Microservice URL
PROD_MICROSERVICE_URL = appsettings['ProductMicroserviceUrl']
category_handler = CategoryHandler(PROD_MICROSERVICE_URL)


@blueprint.route("")
class CategoryListAPI(MethodView):
    @jwt_required()
    def get(self):
        """Retrieve list of all categories (auth required)"""
        try:
            token = request.headers.get('Authorization')  
            categories = category_handler.get_all_category(token=token)

            if not categories:
                abort(404, message="No categories found")

            return jsonify([category.to_dict() for category in categories]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@blueprint.route("/<int:category_id>")
class CategoryByIdAPI(MethodView):
    @jwt_required()
    def get(self, category_id):
        """Retrieve a single category by its ID (auth required)"""
        try:
            token = request.headers.get('Authorization')  # ✅ get token
            category = category_handler.get_product_by_id(category_id, token=token)

            if not category:
                abort(404, message=f"Category with id {category_id} not found")

            return jsonify(category.to_dict()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Register blueprint
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
