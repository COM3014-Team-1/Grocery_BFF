import requests
from config import appsettings
from Application.user.login.logindto import LoginDTO
from Application.user.login.logindto import UserServiceLoginSchema
from Application.seed.seed import Seed
import json

USER_MICROSERVICE_URL = appsettings['UserMicroserviceUrl']  #load the url from appsetting.{env}.config

class LoginHandler:
    @staticmethod
    def login(login_dto: LoginDTO):
        try:
            user_service_payload = UserServiceLoginSchema.from_login_dto(login_dto)
        
            print("****** Payload to User Microservice:")
            print(json.dumps(user_service_payload, indent=2))  # pretty-print as JSON

            response = requests.post(
                f"{USER_MICROSERVICE_URL}/api/auth/login",
                json=user_service_payload 
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
