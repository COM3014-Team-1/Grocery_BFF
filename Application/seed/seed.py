from Application.product.getproduct.getproductvm import ProductVM  # Import the ProductVM class

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

    @staticmethod
    def get_dummy_products():
        return {
            "status": "success",
            "data": [
                ProductVM(1, "Cauliflower", 1.25, 100, 3, "https://grocery-brainybites.s3.eu-west-2.amazonaws.com/cauliflower.jpg", 4.5, True, True, "Vegetables"),
                ProductVM(2, "Organic Carrot", 2.99, 50, 1, "https://grocery-brainybites.s3.eu-west-2.amazonaws.com/carrot.jpg", 4.2, True, False, "Vegetables"),
                ProductVM(3, "White Bread", 1.75, 75, 2, "https://grocery-brainybites.s3.eu-west-2.amazonaws.com/bread.jpg", 4.0, True, True, "Bakery"),
                ProductVM(4, "Chicken", 5.49, 30, 4, "https://grocery-brainybites.s3.eu-west-2.amazonaws.com/chicken.jpg", 4.7, True, True, "Meat")
            ]
        }
