import requests
from datetime import datetime
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
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_data = {
            "username": name,
            "email": email,
            "password": password,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "created_at": now,
            "updated_at": now,
            "last_login": now
        }
        
        # Send the data to the user service's signup endpoint
        response = self.client.post(f"{self.user_service_url}/api/auth/register", json=user_data)
        
        if response.status_code != 200:
            # Handle error in response
            response.raise_for_status()  # Raises HTTPError if the response code is 4xx/5xx
        
        # Merge the user data from User Microservice into the expected UserVM format
        user_data = response.json().get("user", {})
        
        # Manually create the UserVM instance using the merged data
        user_vm = UserVM(
            user_id=user_data.get("user_id"),
            username=user_data.get("name"),
            email=user_data.get("email"),
            phone=user_data.get("phone"),
            address=user_data.get("address"),
            city=user_data.get("city"),
            state=user_data.get("state"),
            zipcode=user_data.get("zipcode"),
            created_at=user_data.get("created_at")
        )
        
        # Return the UserVM instance to be used by the frontend
        return user_vm
