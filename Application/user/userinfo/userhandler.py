import uuid
import requests
from Application.user.userinfo.getuserdto import GetUserDTO
from Application.user.userinfo.getuservm import UserVM
from config import appsettings
'''
def get_user_handler(user_id: int) -> GetUserVM:
    return {"message": "Successfully called handler from API", "user_id": user_id}
'''

from typing import Optional

USER_MICROSERVICE_URL = appsettings['UserMicroserviceUrl']

class UserHandler:

    def __init__(self, USER_MICROSERVICE_URL: str):
        self.user_service_url = USER_MICROSERVICE_URL
        print(f"****** URL of user microservice: {USER_MICROSERVICE_URL}")
        self.client = requests.Session()

    def _get_auth_headers(self, token: str):
        """Helper function to return headers with the token"""
        return {"Authorization": f"{token}"} if token else {}

    def get_user_by_id(self, user_id: uuid, jwt_token: str) -> Optional[UserVM]:
        """Retrieve a user by their user ID from the user microservice."""
        headers = self._get_auth_headers(jwt_token)
        # Send GET request to fetch cart items
        url = f"{self.user_service_url}/api/auth/user/{user_id}"
        print(f"****** Calling user microservice at: {url}")

        response = self.client.get(url, headers=headers)

        if response.status_code == 404:
            print("****** User not found.")
            return None

        response.raise_for_status()
        user_json = response.json()

        return UserVM.from_dict(user_json)

    def edit_user(self, user_id, data, token):
        # Get headers with the Authorization token
        headers = self._get_auth_headers(token)

        response = self.client.put(
            f"{self.user_service_url}/api/auth/user/{user_id}/edit",
            json=data,
            headers=headers
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return UserVM.from_dict(response.json())


