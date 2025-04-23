from flask import Flask, jsonify, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from Application.user.userinfo.edituserdto import EditUserDTO
from Application.user.userinfo.userhandler import UserHandler
from Application.user.login.logindto import LoginDTO
from Application.user.login.loginhandler import LoginHandler
from Application.user.login.loginvm import LoginVM
from Application.user.signup.signuphandler import SignupHandler
from Application.user.signup.signupdto import SignupDTO
from Application.user.userinfo.getuservm import UserVM
from config import appsettings
from flask_jwt_extended import jwt_required
from flask import make_response

# Initialize Flask app
app = Flask(__name__)

# Create Flask-Smorest blueprint
blueprint = Blueprint("users", __name__, url_prefix="/user", description="User Management")
USER_MICROSERVICE_URL = appsettings['UserMicroserviceUrl']  # Load the URL from appsettings

# ----------------------------------------
# Login Endpoint (no token required)
# ----------------------------------------
@blueprint.route("/login", methods=["POST"])
class LoginAPI(MethodView):
    @blueprint.arguments(LoginDTO)
    def post(self, data):
        """User Login API to store token in cookies"""
        try:
            print("****login with cookie**********")
            user_response, status_code = LoginHandler.login(data)

            if status_code == 200:
                login_vm = LoginVM.from_json(user_response)
                response = make_response(jsonify(login_vm.to_dict()), 200)

                # Extract token
                token = login_vm.token

                # Set it in an HTTP-only cookie
                response.set_cookie(
                    key='token',
                    value=token,
                    httponly=False,         # Ensure it's set to True in production (for security)
                    secure=False,           # Set to True if using HTTPS
                    samesite='Lax',        # Or 'Strict' / 'None' based on your setup
                    max_age=3600           # 1 hour expiration
                )

                # Log the cookie being set for debugging
                print("*******Set-Cookie header:", response.headers.get('Set-Cookie'))

                return response

            return jsonify({"message": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500
# ----------------------------------------
# Logout API - Clear Token Cookie
# ----------------------------------------
@blueprint.route("/logout", methods=["POST"])
class LogoutAPI(MethodView):
    def post(self):
        """Logs the user out by clearing the token cookie."""
        response = make_response(jsonify({"message": "Logout successful"}), 200)

        # Clear the token cookie
        response.set_cookie(
            key='token',
            value='',
            expires=0,          # Expire immediately
            httponly=False,     # Should match what you used during login
            secure=False,       # Match your login setup
            samesite='Lax'      # Consistent with login setup
        )
        return response


# ----------------------------------------
# Signup Endpoint
# ----------------------------------------
@blueprint.route("/signup", methods=["POST"])
class UserSignupAPI(MethodView):
    @blueprint.arguments(SignupDTO)
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

            if user:
                return jsonify(user.to_dict()), 201

            abort(400, message="Signup failed. Please try again.")

        except Exception as e:
            return jsonify({"error": str(e)}), 500

# ----------------------------------------
# Get User by ID (Token Required)
# ----------------------------------------
@blueprint.route("/user/<uuid:user_id>", methods=["GET"])
class GetUserAPI(MethodView):
    @jwt_required()
    def get(self, user_id):
        """Retrieve a user by their user ID"""
        try:
            jwt_token = request.headers.get('Authorization')  # Bearer token

            get_user_handler = UserHandler(USER_MICROSERVICE_URL)
            user = get_user_handler.get_user_by_id(user_id, jwt_token)

            if user:
                return jsonify(user.to_dict()), 200
            else:
                return jsonify({"message": "User not found"}), 404

        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ----------------------------------------
# Edit User by ID (Token Required)
# ----------------------------------------
@blueprint.route("/user/<uuid:user_id>/edit", methods=["PUT"])
class EditUserAPI(MethodView):
    @jwt_required()
    @blueprint.arguments(EditUserDTO)
    def put(self, data, user_id):
        """Edit user details"""
        try:
            jwt_token = request.headers.get("Authorization")
            handler = UserHandler(USER_MICROSERVICE_URL)
            updated_user = handler.edit_user(user_id, data, jwt_token)

            if updated_user:
                return jsonify(updated_user.to_dict()), 200
            return jsonify({"message": "User not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
# Register blueprint
app.register_blueprint(blueprint)

# Run the app directly if needed
if __name__ == "__main__":
    app.run(debug=True)
