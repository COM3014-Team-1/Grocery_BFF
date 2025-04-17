import requests
import copy

class OrderHandler:
    def __init__(self, order_service_url: str):
        self.order_service_url = order_service_url
        self.client = requests.Session()

    def get_user_orders(self, user_id: str):
        url = f"{self.order_service_url}/users/{user_id}/orders"
        response = self.client.get(url)

        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

    def get_order_by_id(self, order_id):
        response = self.client.get(f"{self.order_service_url}/orders/{order_id}")

        if response.status_code == 404:
            return None  # or raise error if you want

        response.raise_for_status()
        return response.json()

    def create_order(self, data):
        # Sanitize UUIDs to strings
        sanitized_data = copy.deepcopy(data)
        if 'user_id' in sanitized_data:
            sanitized_data['user_id'] = str(sanitized_data['user_id'])

        for item in sanitized_data.get('order_items', []):
            if 'product_id' in item:
                item['product_id'] = str(item['product_id'])

        response = self.client.post(f"{self.order_service_url}/orders", json=sanitized_data)
        response.raise_for_status()
        return response.json()

    def update_order(self, order_id, order_data):
        # Make a safe copy to sanitize UUIDs
        sanitized_data = copy.deepcopy(order_data)

        if 'user_id' in sanitized_data:
            sanitized_data['user_id'] = str(sanitized_data['user_id'])

        for item in sanitized_data.get('order_items', []):
            if 'product_id' in item:
                item['product_id'] = str(item['product_id'])

        # Send sanitized data to the microservice
        response = self.client.put(f"{self.order_service_url}/orders/{order_id}", json=sanitized_data)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()

    def cancel_order(self, order_id):
        response = self.client.delete(f"{self.order_service_url}/orders/{order_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
