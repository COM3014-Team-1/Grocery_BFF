from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from Application.user.getuser.getuserhandler import get_user_handler
from Application.user.login.logindto import LoginDTO
from Application.user.login.loginhandler import LoginHandler
from Application.user.login.loginvm import LoginVM

blueprint = Blueprint("users", __name__, url_prefix="/user", description="User Management")

@blueprint.route("/<int:user_id>")
class UserAPI(MethodView):
    def get(self, user_id):
        """Get User by ID"""
        user_data = get_user_handler(user_id)
        return jsonify(user_data)

@blueprint.route("/login")
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
