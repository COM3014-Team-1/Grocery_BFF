from flask import Flask, abort, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from Application.order.cart.addtocartdto import AddToCartDTO
from Application.order.cart.carthandler import CartHandler
from Application.order.cart.removeitemfromcartdto import RemoveFromCartDTO
from Application.order.cart.updateitemcartdto import CartItemUpdateDTO
from Application.order.getorder.orderdto import OrderDTO
from Application.order.getorder.orderhistoryvm import GetOrderHistoryVM
from Application.order.getorder.orderwithorderitemsvm import OrderVM
from Application.order.getorder.orderhandler import OrderHandler 
from config import appsettings
from marshmallow import ValidationError
import json
from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT-related functions

# Initialize Flask app and blueprint
app = Flask(__name__)
blueprint = Blueprint("orders", __name__, url_prefix="/order", description="Order Management")
ORDER_MICROSERVICE_URL = appsettings['OrderMicroserviceUrl']  # Load the URL from appsettings

@blueprint.route('/cart/<uuid:user_id>', methods=['GET'])
class GetUserCartAPI(MethodView):
    @jwt_required()
    def get(self, user_id):
        """Fetch the cart for a specific user with product details"""
        jwt_user = get_jwt_identity()
        if jwt_user != str(user_id):
            return jsonify({"error": "Unauthorized"}), 401

        try:
            cart_handler = CartHandler(ORDER_MICROSERVICE_URL)
            
            jwt_token = request.headers.get('Authorization')

            # Step 1: Get cart items
            cart_items = cart_handler.get_user_cart(user_id, jwt_token)

            # Step 2: Enrich with product info
            enriched_cart = []
            for item in cart_items:
                cart_dict = item.to_dict()
                try:
                    print("*****product id: "+item.product_id)
                    product_info = cart_handler.get_product_info(item.product_id, jwt_token)
                    cart_dict["product_name"] = product_info.get("name")
                    cart_dict["image_url"] = product_info.get("image_url")
                except Exception as ex:
                    cart_dict["product_name"] = "Unknown"
                    cart_dict["image_url"] = ""
                    print(f"Failed to fetch product for {item.product_id}: {ex}")

                enriched_cart.append(cart_dict)

            enriched_cart.sort(key=lambda x: str(x["product_id"]))
            return jsonify(enriched_cart), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/cart/add", methods=["POST"])
class AddToCartAPI(MethodView):
    @jwt_required()
    @blueprint.arguments(AddToCartDTO)
    def post(self, data):
        jwt_user = get_jwt_identity()
        token = request.headers.get('Authorization')
        if not jwt_user:
            return jsonify({"error": "Unauthorized"}), 401

        try:
            handler = CartHandler(ORDER_MICROSERVICE_URL)
            
            # Step 1: Add to cart via Order MS
            cart_item = handler.add_to_cart(
                user_id=data['user_id'],
                product_id=data['product_id'],
                quantity=data['quantity'],
                unit_price=data['unit_price'],
                token=token
            )

            cart_dict = cart_item.to_dict()

            # Step 2: Fetch product info from Product MS
            product_info = handler.get_product_info(data['product_id'], token)

            # Step 3: Merge product info into cart item response
            if product_info:
                cart_dict["product_name"] = product_info.get("name")
                cart_dict["image_url"] = product_info.get("image_url")

            return jsonify(cart_dict), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/cart/remove", methods=["DELETE"])
class RemoveFromCartAPI(MethodView):
    @jwt_required()
    @blueprint.arguments(RemoveFromCartDTO)
    def delete(self, data):
        """Remove items from cart"""
        try:
            token = request.headers.get("Authorization")
            handler = CartHandler(ORDER_MICROSERVICE_URL)

            user_id = data["user_id"]
            products = data["products"]

            result = handler.remove_from_cart(user_id, products, token)

            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/cart/update/<string:product_id>", methods=["PUT"])
class UpdateCartQuantityAPI(MethodView):
    @jwt_required()
    @blueprint.arguments(CartItemUpdateDTO)
    def put(self, data, product_id):
        """Update quantity of an item in the cart"""
        try:
            token = request.headers.get("Authorization")
            handler = CartHandler(ORDER_MICROSERVICE_URL)

            quantity = data["quantity"]
            result = handler.update_cart_quantity(product_id, quantity, token)

            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "Cart item not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/user/<string:user_id>/orders", methods=["GET"])
class GetUserOrdersAPI(MethodView):
    @jwt_required()  # Ensure token is required
    def get(self, user_id):
        jwt_user = get_jwt_identity()  # Get user identity from the token
        if jwt_user != user_id:
            return jsonify({"error": "Unauthorized"}), 401

        try:
            token = request.headers.get("Authorization")  # Pass the JWT token to the handler
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            order_list = handler.get_user_orders(user_id, token)

            order_vm_list = OrderVM.from_list(order_list)
            return jsonify([order.to_dict() for order in order_vm_list]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/<order_id>", methods=["GET"])
class GetOrderHistoryAPI(MethodView):
    @jwt_required()  # Ensure token is required
    def get(self, order_id):
        jwt_user = get_jwt_identity()  # Get user identity from the token

        if not jwt_user:  # Ensure valid token
            return jsonify({"error": "Unauthorized"}), 401

        try:
            token = request.headers.get("Authorization")  # Pass the JWT token to the handler
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            order_data = handler.get_order_by_id(order_id,token)

            if not order_data:
                abort(404, message="Order not found")

            vm = GetOrderHistoryVM.from_dict(order_data)
            return jsonify(vm.to_dict()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/create", methods=["POST"])
class CreateOrderAPI(MethodView):
    @jwt_required()  # Ensure token is required
    @blueprint.arguments(OrderDTO)
    def post(self, data):
        jwt_user = get_jwt_identity()  # Get user identity from the token
        if not jwt_user:  # Ensure valid token
            return jsonify({"error": "Unauthorized"}), 401

        try:
            token = request.headers.get("Authorization")  # Pass the JWT token to the handler
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            result = handler.create_order(data, token)

            return Response(json.dumps(result, default=str), mimetype="application/json", status=201)

        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/update/<order_id>", methods=["PUT"])
class UpdateOrderAPI(MethodView):
    @jwt_required()  # Ensure token is required
    @blueprint.arguments(OrderDTO(partial=True))
    def put(self, data, order_id):
        jwt_user = get_jwt_identity()  # Get user identity from the token
        if not jwt_user:  # Ensure valid token
            return jsonify({"error": "Unauthorized"}), 401

        try:
            token = request.headers.get("Authorization")  # Pass the JWT token to the handler
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            result = handler.update_order(order_id, data, token)
            if not result:
                return jsonify({"message": "Order not found"}), 404
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/cancel/<order_id>", methods=["DELETE"])
class CancelOrderAPI(MethodView):
    @jwt_required()  # Ensure token is required
    def delete(self, order_id):
        jwt_user = get_jwt_identity()  # Get user identity from the token
        if not jwt_user:  # Ensure valid token
            return jsonify({"error": "Unauthorized"}), 401

        try:
            token = request.headers.get("Authorization")  # Pass the JWT token to the handler
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            result = handler.cancel_order(order_id, token)
            if not result:
                return jsonify({"message": "Order not found or already cancelled"}), 404
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Register blueprint with the Flask app
app.register_blueprint(blueprint)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
