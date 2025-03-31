import requests
from config import appsettings
from Application.user.login.logindto import LoginDTO
from Application.seed.seed import Seed

USER_MICROSERVICE_URL = appsettings['UserMicroserviceUrl'] #load the url from appsetting.{env}.config

class LoginHandler:
    @staticmethod
    def login(login_dto: LoginDTO):
        try:
            return Seed.get_dummy_login(), 200 # will remove this when the user ms api is ready to use
            ## temporarily comment out calling user ms
            # response = requests.post(USER_MICROSERVICE_URL, json=login_dto.to_dict())
            # return reponse.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500