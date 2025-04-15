import requests
from Application.order.getorder.cartitemvm import CartItemVM 
from config import appsettings

class CartHandler:
    def __init__(self, order_service_url):
        self.order_service_url = order_service_url
        self.client = requests.Session()

    def add_to_cart(self, user_id, product_id, quantity, unit_price):
        payload = {
            "user_id": str(user_id),
            "product_id": str(product_id),
            "quantity": quantity,
            "unit_price": str(unit_price)
        }

        response = self.client.post(f"{self.order_service_url}/cart", json=payload)
        response.raise_for_status()
        return CartItemVM.from_dict(response.json())
