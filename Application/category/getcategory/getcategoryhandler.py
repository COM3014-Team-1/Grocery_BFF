from typing import List, Optional
from Application.seed.seed import Seed
from config import appsettings
from Application.category.getcategory.categoryvm import CategoryVM
import requests  # For future real service calls

PROD_MICROSERVICE_URL = appsettings['ProductMicroserviceUrl'] #load the url from appsetting.{env}.config

class CategoryHandler:

    def __init__(self, PROD_MICROSERVICE_URL: str):
        self.product_service_url = PROD_MICROSERVICE_URL
        print(f"******url of prod ms: "+PROD_MICROSERVICE_URL)
        self.client = requests.Session()

    def get_all_category(self, search: Optional[str] = None) -> List[CategoryVM]:
        response = self.client.get(f"{PROD_MICROSERVICE_URL}/categories")
         
        response.raise_for_status()
        print(f"***** Response from category: {response.json()}")

        category_json = response.json()
        return [CategoryVM.from_dict(category) for category in category_json]
        

    def get_product_by_id(self, category_id: int) -> Optional[CategoryVM]:
        """Retrieve a single category by its ID."""

        response = self.client.get(f"{self.product_service_url}/categories/{category_id}")
        response.raise_for_status()
        return CategoryVM.from_dict(response.json())
