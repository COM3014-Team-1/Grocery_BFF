import requests
from Application.user.getuser.getuserdto import GetUserDTO
from Application.user.getuser.getuservm import GetUserVM
from config import appsettings

def get_user_handler(user_id: int) -> GetUserVM:
    return {"message": "Successfully called handler from API", "user_id": user_id}
