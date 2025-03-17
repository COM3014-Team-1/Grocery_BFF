from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from API.usercontroller import user_controller
from Application.user.getuser.getuserhandler import get_user_handler  # Import the handler
from config import appsettings

app = Flask(__name__)

# Print to verify the configuration
print("MICROSERVICE_URL:", appsettings['MICROSERVICE_URL'])

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Grocery Online Shopping BFF"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "BFF is running"}), 200

# User Endpoint (call the actual handler instead of returning hardcoded data)
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_data = get_user_handler(user_id)  # Call the real handler
    return jsonify(user_data)

# Order Endpoint
@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    return jsonify({"order_id": order_id, "status": "Completed"})

# Product Endpoint
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return jsonify({"product_id": product_id, "name": "Apple", "price": 1.2})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
