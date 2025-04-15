from marshmallow import Schema, fields, validate

class AddToCartDTO(Schema):
    user_id = fields.UUID(required=True)
    product_id = fields.UUID(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    unit_price = fields.Decimal(required=True, as_string=True)
