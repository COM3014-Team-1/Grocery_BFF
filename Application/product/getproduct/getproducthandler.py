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
        
        # Uncomment this for real microservice connection
        #response = self.client.get(f"{self.product_service_url}/products", params={"search": search} if search else {})
        print(f"******url of prod ms: {PROD_MICROSERVICE_URL}/products")   
        response = self.client.get(f"{PROD_MICROSERVICE_URL}/products")
         
        response.raise_for_status()
        print(f"***** Response from product: {response.json()}")

        products_json = response.json()
        return [ProductVM.from_dict(prod) for prod in products_json]
        

    def get_product_by_id(self, product_id: int) -> Optional[ProductVM]:
        """Retrieve a single product by its ID."""

        # Get dummy data from Seed (already as ProductVM instances)
        product_data = Seed.get_dummy_products()
        all_products = product_data['data']

        return next((prod for prod in all_products if prod.product_id == product_id), None)

        '''
        # Uncomment this for real microservice connection
        response = self.client.get(f"{self.product_service_url}/products/{product_id}")
        response.raise_for_status()
        return ProductVM.from_dict(response.json())
        '''
