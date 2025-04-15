from flask import Flask, jsonify
from flask_smorest import Api  # Import Flask-Smorest API
from flask_swagger_ui import get_swaggerui_blueprint
import importlib
import pkgutil
from flask_cors import CORS

# Import controllers
from API import usercontroller, productcontroller

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Enable Flask-Smorest OpenAPI Specification
app.config["API_TITLE"] = "Grocery Online Shopping BFF"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"  # Ensure /openapi.json is generated

api = Api(app)  # Attach Flask-Smorest API

# Auto Register Blueprints from API folder
def register_blueprints():
    """Automatically registers all API blueprints inside API folder."""
    for _, module_name, _ in pkgutil.iter_modules(["API"]):
        module = importlib.import_module(f"API.{module_name}")
        if hasattr(module, "blueprint"):  
            api.register_blueprint(module.blueprint)  # Register using Flask-Smorest
            print(f"✔ Registered: {module_name}")

register_blueprints()

# Swagger UI Setup
SWAGGER_URL = "/swagger"
API_URL = "/openapi.json"  # Auto-generated OpenAPI JSON
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Grocery Online Shopping BFF"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Health Check Endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "BFF is running"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
