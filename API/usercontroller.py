from flask import Flask, jsonify, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from Application.user.getuser.getuserhandler import UserHandler
from Application.user.login.logindto import LoginDTO
from Application.user.login.loginhandler import LoginHandler
from Application.user.login.loginvm import LoginVM
from Application.user.signup.signuphandler import SignupHandler
from Application.user.signup.signupdto import SignupDTO
from Application.user.getuser.getuservm import UserVM
from config import appsettings
import uuid

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

# Define the API to retrieve user details by ID
@blueprint.route("/user/<uuid:user_id>", methods=["GET"])
class GetUserAPI(MethodView):
    def get(self, user_id):
        """Retrieve a user by their user ID"""
        try:
            # Get the JWT token from request headers
            jwt_token = request.headers.get('Authorization')

            # Call the handler to fetch user details
            get_user_handler = UserHandler(USER_MICROSERVICE_URL)
            user = get_user_handler.get_user_by_id(user_id, jwt_token)

            if user:
                # If user is found, return user details
                return jsonify(user.to_dict()), 200
            else:
                # If user is not found, return 404 error
                return jsonify({"message": "User not found"}), 404

        except Exception as e:
            # Catch any errors and return error message
            print(f"Error getting user: {str(e)}")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Register blueprint with the Flask app
app.register_blueprint(blueprint)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

