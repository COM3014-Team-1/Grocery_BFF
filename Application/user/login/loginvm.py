class LoginVM:
    def __init__(self, token, user_id, name):
        self.token = token
        self.user = {
            "id": user_id,
            "name": name
        }

    def to_dict(self):
        """Convert instance to a dictionary for JSON serialization."""
        return {
            "token": self.token,
            "user": self.user
        }

    @staticmethod
    def from_json(data):
        """
        Convert response data to a LoginVM instance.
        Extract `token`, `user_id`, and `username` from the response.
        """
        token = data.get("token")
        user_data = data.get("user", {})

        # Extract user_id and username from the user data.
        user_id = user_data.get("user_id")
        name = user_data.get("name")  # Assuming 'name' is the equivalent of 'username'

        return LoginVM(token=token, user_id=user_id, name=name)
