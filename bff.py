from flask import Flask, jsonify
from flask_smorest import Api
from flask_swagger_ui import get_swaggerui_blueprint
import importlib
import pkgutil
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import appsettings

# Import controllers
from API import usercontroller, productcontroller, ordercontroller

app = Flask(__name__)

# === Flask config setup ===
app.config["SECRET_KEY"] = appsettings["SECRET_KEY"]
app.config["JWT_SECRET_KEY"] = appsettings["SECRET_KEY"]  # Used for JWT token validation

# === JWT Setup ===
jwt = JWTManager(app)

# === CORS ===
CORS(app, supports_credentials=True)

# === Flask-Smorest / Swagger Config ===
app.config["API_TITLE"] = "Grocery Online Shopping BFF"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI"] = True
app.config["OPENAPI_SWAGGER_UI_AUTH"] = True

# Enable Authorization via Bearer token
app.config["OPENAPI_SECURITY_SCHEMES"] = {
    "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}

# === Flask-Smorest API Setup ===
api = Api(app)

api.spec.components.security_scheme("bearerAuth", {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
})
api.spec.options["security"] = [{"bearerAuth": []}]

# === Auto-register blueprints ===
def register_blueprints():
    """Automatically registers all API blueprints inside API folder."""
    for _, module_name, _ in pkgutil.iter_modules(["API"]):
        module = importlib.import_module(f"API.{module_name}")
        if hasattr(module, "blueprint"):
            api.register_blueprint(module.blueprint)
            print(f"✔ Registered: {module_name}")

register_blueprints()

# === Swagger UI Setup ===
SWAGGER_URL = "/swagger"
API_URL = "/openapi.json"  # This is what Flask-Smorest generates

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Grocery Online Shopping BFF"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# === Health Check ===
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "BFF is running"}), 200

# === Run ===
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
