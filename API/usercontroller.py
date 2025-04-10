from flask import Flask, jsonify, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from Application.user.login.logindto import LoginDTO
from Application.user.login.loginhandler import LoginHandler
from Application.user.login.loginvm import LoginVM
from Application.user.signup.signuphandler import SignupHandler
from Application.user.signup.signupdto import SignupDTO
from Application.user.getuser.getuservm import UserVM  # Ensure you have the UserVM import
from config import appsettings

# Initialize Flask app
app = Flask(__name__)

# Create Flask-Smorest blueprint
blueprint = Blueprint("users", __name__, url_prefix="/user", description="User Management")
USER_MICROSERVICE_URL = appsettings['UserMicroserviceUrl']  # Load the URL from appsetting.{env}.config

# Endpoint for user login
@blueprint.route("/login", methods=["POST"])
class LoginAPI(MethodView):
    @blueprint.arguments(LoginDTO)  # Validates input via Swagger
    def post(self, data):
        """User Login API"""
        try:
            # Call handler to process login
            user_response, status_code = LoginHandler.login(data)

            if status_code == 200:
                # Convert to VM format before returning
                login_vm = LoginVM.from_json(user_response)
                return jsonify(login_vm.to_dict()), status_code

            return jsonify({"message": "Invalid credentials"}), 401  

        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint to sign up a new user
@blueprint.route("/signup", methods=["POST"])
class UserSignupAPI(MethodView):
    @blueprint.arguments(SignupDTO)  # Validates input via Swagger
    def post(self, data):
        """Sign up a new user"""
        try:
            signup_handler = SignupHandler(USER_MICROSERVICE_URL)

            user = signup_handler.signup_user(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                phone=data.get('phone'),
                address=data.get('address'),
                city=data.get('city'),
                state=data.get('state'),
                zipcode=data.get('zipcode')
            )

            # If user is successfully created, return the user details
            if user:
                return jsonify(user.to_dict()), 201

            # If signup failed, return an error response
            abort(400, message="Signup failed. Please try again.")

        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Register blueprint with the Flask app
app.register_blueprint(blueprint)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

