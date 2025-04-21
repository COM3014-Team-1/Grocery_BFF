from typing import List, Optional
from Application.seed.seed import Seed
from config import appsettings
from Application.category.getcategory.categoryvm import CategoryVM
import requests

PROD_MICROSERVICE_URL = appsettings['ProductMicroserviceUrl']


class CategoryHandler:
    def __init__(self, product_service_url: str):
        self.product_service_url = product_service_url
        self.client = requests.Session()

    def _get_auth_headers(self, token: str):
        """Helper function to return headers with the token"""
        return {"Authorization": f"{token}"} if token else {}

    def get_all_category(self, token: str, search: Optional[str] = None) -> List[CategoryVM]:
        headers = self._get_auth_headers(token)

        response = self.client.get(f"{self.product_service_url}/categories", headers=headers)
        response.raise_for_status()

        print(f"***** Response from category: {response.json()}")

        category_json = response.json()
        return [CategoryVM.from_dict(category) for category in category_json]

    def get_product_by_id(self, category_id: int, token: str = None) -> Optional[CategoryVM]:
        headers = self._get_auth_headers(token)

        response = self.client.get(f"{self.product_service_url}/categories/{category_id}", headers=headers)
        response.raise_for_status()

        return CategoryVM.from_dict(response.json())
