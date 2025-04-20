import requests
import copy

class OrderHandler:
    def __init__(self, order_service_url: str):
        self.order_service_url = order_service_url
        self.client = requests.Session()

    def _get_auth_headers(self, token):
        return {"Authorization": f"{token}"} if token else {}

    def get_user_orders(self, user_id: str, token=None):
        url = f"{self.order_service_url}/users/{user_id}/orders"
        headers = self._get_auth_headers(token)
        response = self.client.get(url, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    def get_order_by_id(self, order_id, token=None):
        url = f"{self.order_service_url}/orders/{order_id}"
        headers = self._get_auth_headers(token)
        response = self.client.get(url, headers=headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def create_order(self, data, token=None):
        sanitized_data = copy.deepcopy(data)
        if 'user_id' in sanitized_data:
            sanitized_data['user_id'] = str(sanitized_data['user_id'])

        for item in sanitized_data.get('order_items', []):
            if 'product_id' in item:
                item['product_id'] = str(item['product_id'])

        headers = self._get_auth_headers(token)
        response = self.client.post(f"{self.order_service_url}/orders", json=sanitized_data, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_order(self, order_id, order_data, token=None):
        sanitized_data = copy.deepcopy(order_data)
        if 'user_id' in sanitized_data:
            sanitized_data['user_id'] = str(sanitized_data['user_id'])

        for item in sanitized_data.get('order_items', []):
            if 'product_id' in item:
                item['product_id'] = str(item['product_id'])

        headers = self._get_auth_headers(token)
        response = self.client.put(f"{self.order_service_url}/orders/{order_id}", json=sanitized_data, headers=headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def cancel_order(self, order_id, token=None):
        headers = self._get_auth_headers(token)
        response = self.client.delete(f"{self.order_service_url}/orders/{order_id}", headers=headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
