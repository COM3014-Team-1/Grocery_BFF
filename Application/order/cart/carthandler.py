import requests
from Application.order.getorder.cartitemvm import CartItemVM
from typing import List, Optional
from config import appsettings

class CartHandler:
    def __init__(self, order_service_url: str):
        self.order_service_url = order_service_url
        self.client = requests.Session()

    def _get_auth_headers(self, token: str):
        """Helper function to return headers with the token"""
        return {"Authorization": f"{token}"} if token else {}

    def add_to_cart(self, user_id, product_id, quantity, unit_price, token: str):
        """Add a product to the user's cart."""
        payload = {
            "user_id": str(user_id),
            "product_id": str(product_id),
            "quantity": quantity,
            "unit_price": str(unit_price)
        }

        # Get headers with the Authorization token
        headers = self._get_auth_headers(token)

        # Send POST request to add item to cart
        response = self.client.post(f"{self.order_service_url}/cart", json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception if request fails

        # Return CartItemVM from response
        return CartItemVM.from_dict(response.json())

    def get_user_cart(self, user_id: str, token: str) -> List[CartItemVM]:
        """Fetch the cart items for a specific user."""
        
        # Construct URL for the API
        url = f"{self.order_service_url}/cart/{user_id}"
        # Get headers with the Authorization token
        headers = self._get_auth_headers(token)
        # Send GET request to fetch cart items
        response = self.client.get(url, headers=headers)
        
        if response.status_code != 200:
            response.raise_for_status()  # Raise an error if not successful

        # Map the response data to ViewModel (CartItemVM) and return it
        cart_items = response.json()
        return [CartItemVM.from_dict(item) for item in cart_items]

    def remove_from_cart(self, user_id, products, token):
        url = f"{self.order_service_url}/cartItems"

        # Get headers with the Authorization token
        headers = self._get_auth_headers(token)

        payload = {
            "user_id": str(user_id),
            "products": [str(p) for p in products]
        }

        response = self.client.delete(url, headers=headers, json=payload)
    
        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()
