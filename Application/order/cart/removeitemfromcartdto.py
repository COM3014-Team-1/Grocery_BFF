from marshmallow import Schema, fields
from uuid import UUID

class RemoveFromCartDTO(Schema):
    user_id = fields.UUID(required=True)
    products = fields.List(fields.UUID(), required=True)