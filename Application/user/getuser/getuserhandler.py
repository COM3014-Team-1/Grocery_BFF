import requests
from Application.user.getuser.getuserdto import GetUserDTO
from Application.user.getuser.getuservm import GetUserVM
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

    def get_user_by_id(self, user_id: int, jwt_token: str) -> Optional[GetUserVM]:
        """Retrieve a user by their user ID from the user microservice."""
        '''
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
        '''
        url = f"{self.user_service_url}/user/{user_id}"
        print(f"****** Calling user microservice at: {url}")

        response = self.client.get(url) #, headers=headers) when the authorization check is ready

        if response.status_code == 404:
            print("****** User not found.")
            return None

        response.raise_for_status()
        user_json = response.json()

        print(f"****** Response from user microservice: {user_json}")
        return GetUserVM.from_dict(user_json)


