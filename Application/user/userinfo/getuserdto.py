import uuid

class GetUserDTO:
    def __init__(self, user_id: uuid):
        self.user_id = user_id
