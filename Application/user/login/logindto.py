from marshmallow import Schema, fields

class LoginDTO(Schema):
    """Schema for login request validation"""
    username = fields.String(required=True, description="User's username")
    password = fields.String(required=True, description="User's password")

    @staticmethod
    def from_json(data):
        """Create a LoginDTO instance from JSON"""
        return {"username": data.get("username"), "password": data.get("password")}

    def to_dict(self):
        """Convert instance to dictionary"""
        return {"username": self.username, "password": self.password}
