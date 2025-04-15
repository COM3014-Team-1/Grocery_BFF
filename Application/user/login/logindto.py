from marshmallow import Schema, fields
from datetime import datetime

class LoginDTO(Schema):
    """Schema for login request validation"""
    email = fields.String(required=True, description="User's email")
    password = fields.String(required=True, description="User's password")

    @staticmethod
    def from_json(data):
        """Create a LoginDTO instance from JSON"""
        return {"email": data.get("email"), "password": data.get("password")}

    def to_dict(self):
        """Convert instance to dictionary"""
        return {"email": self.email, "password": self.password}

class UserServiceLoginSchema(Schema):
    identifier = fields.String(required=True)
    password = fields.String(required=True)
    remember_me = fields.Boolean(missing=False)
    created_at = fields.DateTime(missing=lambda: datetime.now())
    updated_at = fields.DateTime(missing=lambda: datetime.now())
    last_login = fields.DateTime(missing=lambda: datetime.now())

    @staticmethod
    def from_login_dto(login_data):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return {
            "identifier": login_data["email"],
            "password": login_data["password"],
            "remember_me": False,
            "created_at": now,
            "updated_at": now,
            "last_login": now
        }