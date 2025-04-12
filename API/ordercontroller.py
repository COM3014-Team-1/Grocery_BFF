from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from Application.order.getorder.getorderhandler import OrderHandler  # Import the OrderHandler
from config import appsettings

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
            order_handler = OrderHandler(ORDER_MICROSERVICE_URL)

            # Fetch cart items for the user
            cart_items = order_handler.get_user_cart(user_id)

            # Return the cart items in the desired format
            return jsonify([item.to_dict() for item in cart_items]), 200

        except Exception as e:
            # Handle errors if the cart retrieval fails
            return jsonify({"error": str(e)}), 500

# Register blueprint with the Flask app
app.register_blueprint(blueprint)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
