from marshmallow import Schema, fields

class EditUserDTO(Schema):
    username = fields.String(required=False)
    email = fields.String(required=False)
    phone = fields.String(required=False)
    address = fields.String(required=False)
    city = fields.String(required=False)
    state = fields.String(required=False)
    zipcode = fields.String(required=False)
