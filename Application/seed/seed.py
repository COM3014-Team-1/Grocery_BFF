class Seed:
    @staticmethod
    def get_dummy_login():
        return {
            "token": "dummy_jwt_token_123",
            "user": {
                "id": "123456",
                "username": "testuser"
            }
        }

    @staticmethod
    def get_dummy_user():
        return {
            "id": "123456",
            "username": "testuser",
            "email": "testuser@example.com"
        }

    @staticmethod
    def get_dummy_orders():
        return [
            {"order_id": "ORD001", "status": "Processing"},
            {"order_id": "ORD002", "status": "Shipped"}
        ]
