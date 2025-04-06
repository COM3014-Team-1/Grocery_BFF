# Application/product/getproduct/getproductdto.py
from marshmallow import Schema, fields

class ProductDTO:
    def __init__(self, search=None):
        self.search = search

class ProductDTOSchema(Schema):
    search = fields.Str(required=False)
