from marshmallow import Schema, fields, pre_load, post_dump, validate

class OrderItemDTO(Schema):
    product_id = fields.UUID(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    unit_price = fields.Float(required=True, validate=validate.Range(min=0))

class OrderDTO(Schema):
    user_id = fields.UUID(required=True)
    shipping_address= fields.String(required=True)
    total_amount = fields.Float(required=True, validate=validate.Range(min=0))
    order_status = fields.String(
        required=True,
        validate=validate.OneOf(["pending", "shipped", "delivered", "cancelled"])
    )
    order_items = fields.Nested(OrderItemDTO, many=True, required=True)

