class LoginVM:
    def __init__(self, token, user_id, username):
        self.token = token
        self.user = {
            "id": user_id,
            "username": username
        }

    def to_dict(self):
        return{
            "token": self.token,
            "user": self.user
        }

    @staticmethod
    def from_json(data):
        return LoginVM(
            token = data.get("token"),
            user_id = data.get("user", {}).get("id"),
            username = data.get("user", {}).get("username")
        )