import requests
from Application.order.getorder.cartitemvm import CartItemVM 
from typing import List, Optional
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

    def get_user_cart(self, user_id: str) -> List[CartItemVM]:
        """Fetch the cart items for a specific user."""
        
        # Construct URL for the API
        url = f"{self.order_service_url}/cart/{user_id}"

        response = self.client.get(url)
        
        if response.status_code != 200:
            response.raise_for_status()  # Raise an error if not successful

        # Map the response data to ViewModel (CartItemVM) and return it
        cart_items = response.json()
        return [CartItemVM.from_dict(item) for item in cart_items]
