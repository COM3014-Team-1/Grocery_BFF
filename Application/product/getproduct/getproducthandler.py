from typing import List, Optional
from Application.seed.seed import Seed
from config import appsettings
from Application.product.getproduct.getproductvm import ProductVM
import requests  # For future real service calls

PROD_MICROSERVICE_URL = appsettings['ProductMicroserviceUrl'] #load the url from appsetting.{env}.config

class ProductHandler:

    def __init__(self, PROD_MICROSERVICE_URL: str):
        self.product_service_url = PROD_MICROSERVICE_URL
        print(f"******url of prod ms: "+PROD_MICROSERVICE_URL)
        self.client = requests.Session()

    def get_all_products(self, search: Optional[str] = None) -> List[ProductVM]:
        """Retrieve all products, optionally filtered by search."""

        '''
        # Get dummy data from Seed (already as ProductVM instances)
        product_data = Seed.get_dummy_products()
        all_products = product_data['data']

        # Filter by search keyword if provided
        filtered_products = [
            product for product in all_products
            if search is None or search.lower() in product.name.lower()
        ]

        return filtered_products
        '''
        
        print(f"******url of prod ms: {PROD_MICROSERVICE_URL}/products")   
        response = self.client.get(f"{PROD_MICROSERVICE_URL}/products")
         
        response.raise_for_status()
        print(f"***** Response from product: {response.json()}")

        products_json = response.json()
        return [ProductVM.from_dict(prod) for prod in products_json]
        

    def get_product_by_id(self, product_id: str) -> ProductVM:
        # Step 1: Call product microservice
        product_resp = self.client.get(f"{self.product_service_url}/products/{product_id}")
        product_resp.raise_for_status()
        product_data = product_resp.json()

        # Step 2: Get category name from category_id
        category_id = product_data["category_id"]
        category_resp = self.client.get(f"{self.product_service_url}/categories/{category_id}")
        category_resp.raise_for_status()
        category_data = category_resp.json()
        category_name = category_data.get("name", "Unknown")

        # Step 3: Merge and return
        product_data["category_name"] = category_name
        return ProductVM.from_dict(product_data)
