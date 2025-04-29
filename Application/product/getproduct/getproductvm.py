from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class ProductVM:
    product_id: uuid
    name: str
    price: float
    quantity: int
    category_id: uuid
    image_url: str
    rating: float
    is_halal: bool
    is_vegan: bool
    category_name: str
    description: str

    def __init__(self, product_id: uuid, name: str, price: float, quantity: int,
                 category_id: uuid, image_url: str, rating: float,
                 is_halal: bool, is_vegan: bool, category_name: str, description: str):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category_id = category_id
        self.image_url = image_url
        self.rating = rating
        self.is_halal = is_halal
        self.is_vegan = is_vegan
        self.category_name = category_name
        self.description = description

    # Optional: You can add any custom methods you may need, for example, converting to dictionary
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'rating': self.rating,
            'is_halal': self.is_halal,
            'is_vegan': self.is_vegan,
            'category_name': self.category_name,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data['product_id'],
            data['name'],
            data['price'],
            data['quantity'],
            data['category_id'],
            data['image_url'],
            data['rating'],
            data['is_halal'],
            data['is_vegan'],
            data['category_name'],
            data['description']
        )
