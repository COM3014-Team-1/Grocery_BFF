from flask import Flask, abort, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from Application.order.cart.addtocartdto import AddToCartDTO
from Application.order.cart.carthandler import CartHandler
from Application.order.getorder.orderdto import OrderDTO
from Application.order.getorder.orderhistoryvm import GetOrderHistoryVM
from Application.order.getorder.orderwithorderitemsvm import OrderVM
from Application.order.getorder.orderhandler import OrderHandler  # Import the OrderHandler
from config import appsettings
from marshmallow import ValidationError
import json
from flask import Response

# Initialize Flask app and blueprint
app = Flask(__name__)
blueprint = Blueprint("orders", __name__, url_prefix="/order", description="Order Management")
ORDER_MICROSERVICE_URL = appsettings['OrderMicroserviceUrl']  # Load the URL from appsettings

# Endpoint to get the user's cart
@blueprint.route('/cart/<uuid:user_id>', methods=['GET'])
class GetUserCartAPI(MethodView):
    def get(self, user_id):
        """Fetch the cart for a specific user."""
        try:
            cart_handler = CartHandler(ORDER_MICROSERVICE_URL)

            # Fetch cart items for the user
            cart_items = cart_handler.get_user_cart(user_id)

            # Return the cart items in the desired format
            return jsonify([item.to_dict() for item in cart_items]), 200

        except Exception as e:
            # Handle errors if the cart retrieval fails
            return jsonify({"error": str(e)}), 500

@blueprint.route("/cart/add", methods=["POST"])
class AddToCartAPI(MethodView):
    @blueprint.arguments(AddToCartDTO)
    def post(self, data):
        try:
            handler = CartHandler(ORDER_MICROSERVICE_URL)
            cart_item = handler.add_to_cart(
                user_id=data['user_id'],
                product_id=data['product_id'],
                quantity=data['quantity'],
                unit_price=data['unit_price']
            )
            return jsonify(cart_item.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/user/<string:user_id>/orders", methods=["GET"])
class GetUserOrdersAPI(MethodView):
    def get(self, user_id):
        try:
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            order_list = handler.get_user_orders(user_id)

            order_vm_list = OrderVM.from_list(order_list)
            return jsonify([order.to_dict() for order in order_vm_list]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/<order_id>", methods=["GET"])
class GetOrderHistoryAPI(MethodView):
    def get(self, order_id):
        try:
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            order_data = handler.get_order_by_id(order_id)

            if not order_data:
                abort(404, message="Order not found")

            vm = GetOrderHistoryVM.from_dict(order_data)
            return jsonify(vm.to_dict()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/create", methods=["POST"])
class CreateOrderAPI(MethodView):
    @blueprint.arguments(OrderDTO)
    def post(self, data):
        try:
            print(f"****request: {data}")
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            result = handler.create_order(data)

            return Response(json.dumps(result, default=str), mimetype="application/json", status=201)

        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@blueprint.route("/update/<order_id>", methods=["PUT"])
class UpdateOrderAPI(MethodView):
    @blueprint.arguments(OrderDTO(partial=True))
    def put(self, data, order_id):
        try:
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            result = handler.update_order(order_id, data)
            if not result:
                return jsonify({"message": "Order not found"}), 404
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@blueprint.route("/cancel/<order_id>", methods=["DELETE"])
class CancelOrderAPI(MethodView):
    def delete(self, order_id):
        try:
            handler = OrderHandler(ORDER_MICROSERVICE_URL)
            result = handler.cancel_order(order_id)
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
