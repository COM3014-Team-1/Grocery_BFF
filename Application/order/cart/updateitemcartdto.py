from marshmallow import Schema, fields, validate

class CartItemUpdateDTO(Schema):
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
