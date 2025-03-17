from flask import Blueprint, request, jsonify
from Application.user.getuser.getuserhandler import get_user_handler

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_data = get_user_handler(user_id)
    return jsonify(user_data)
