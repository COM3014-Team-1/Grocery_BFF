from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class CategoryVM:
    category_id: uuid
    name: str
    description: str
    category_imageurl: str

    def __init__(self, category_id: uuid, name: str, description: str, category_imageurl: str):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.category_imageurl = category_imageurl

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'category_imageurl': self.category_imageurl
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data['category_id'],
            data['name'],
            data['description'],
            data['category_imageurl']
        )
