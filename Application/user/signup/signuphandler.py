import requests
from Application.user.getuser.getuservm import UserVM
from config import appsettings
from typing import Optional  

class SignupHandler:
    def __init__(self, user_service_url: str):
        self.user_service_url = user_service_url
        self.client = requests.Session()

    def signup_user(self, name: str, email: str, password: str, phone: Optional[str] = None,
                    address: Optional[str] = None, city: Optional[str] = None,
                    state: Optional[str] = None, zipcode: Optional[str] = None) -> Optional[UserVM]:
        """Sign up a user by sending a POST request to the User Microservice."""
        
        user_data = {
            "name": name,
            "email": email,
            "password": password,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode
        }
        
        # Send the data to the user service's signup endpoint
        response = self.client.post(f"{self.user_service_url}/signup", json=user_data)
        response.raise_for_status()  # Raises HTTPError if the response code is 4xx/5xx
        
        # Assuming the user service returns the user data upon successful signup
        return UserVM.from_dict(response.json())  # Assuming you have a `from_dict()` method in your UserVM
