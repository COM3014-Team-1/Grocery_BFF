from typing import List
import requests
from config import appsettings
from Application.product.getproduct.getproductvm import ProductVM

PRODUCT_MS_URL = appsettings['ProductMicroserviceUrl']

class GetProductByCategoryHandler:
    def __init__(self):
        self.client = requests.Session()
        self.product_service_url = PRODUCT_MS_URL

    def get_products_by_category(self, category_id: str) -> List[ProductVM]:
        # 1. Get category name
        category_resp = self.client.get(f"{self.product_service_url}/categories/{category_id}")
        category_resp.raise_for_status()
        category_data = category_resp.json()
        category_name = category_data.get("name", "Unknown")

        # 2. Get products by category
        products_resp = self.client.get(f"{self.product_service_url}/products/category/{category_id}")
        products_resp.raise_for_status()
        products_data = products_resp.json()

        # 3. Attach category name to each product
        return [
            ProductVM.from_dict({**product, "category_name": category_name})
            for product in products_data
        ]
