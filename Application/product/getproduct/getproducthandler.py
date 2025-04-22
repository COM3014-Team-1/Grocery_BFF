from typing import List, Optional
from Application.seed.seed import Seed
from config import appsettings
from Application.product.getproduct.getproductvm import ProductVM
import requests

PROD_MICROSERVICE_URL = appsettings['ProductMicroserviceUrl']


class ProductHandler:
    def __init__(self, product_service_url: str):
        self.product_service_url = product_service_url
        self.client = requests.Session()

    def _get_auth_headers(self, token: Optional[str]) -> dict:
        """Generate authorization headers"""
        return {"Authorization": f"{token}"} if token else {}

    def get_all_products(self, search: Optional[str] = None, token: Optional[str] = None) -> List[ProductVM]:
        headers = self._get_auth_headers(token)
        url = f"{self.product_service_url}/products"

        # Optionally handle search filter (e.g., /products?search=abc)
        if search:
            url += f"?search={search}"

        response = self.client.get(url, headers=headers)
        response.raise_for_status()

        print(f"***** Response from product: {response.json()}")
        products_json = response.json()
        return [ProductVM.from_dict(prod) for prod in products_json]

    def get_product_by_id(self, product_id: str, token: Optional[str] = None) -> ProductVM:
        headers = self._get_auth_headers(token)

        # Get product details
        product_resp = self.client.get(f"{self.product_service_url}/products/{product_id}", headers=headers)
        product_resp.raise_for_status()
        product_data = product_resp.json()

        # Get category name from category_id
        category_id = product_data.get("category_id")
        category_resp = self.client.get(f"{self.product_service_url}/categories/{category_id}", headers=headers)
        category_resp.raise_for_status()
        category_data = category_resp.json()

        product_data["category_name"] = category_data.get("name", "Unknown")
        return ProductVM.from_dict(product_data)
