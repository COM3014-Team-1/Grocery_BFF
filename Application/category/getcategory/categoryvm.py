from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class CategoryVM:
    category_id: uuid
    name: str
    description: str

    def __init__(self, category_id: uuid, name: str, description: str):
        self.category_id = category_id
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data['category_id'],
            data['name'],
            data['description']
        )
