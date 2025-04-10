from marshmallow import Schema, fields, validate

class SignupDTO(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True)
    phone = fields.Str()
    address = fields.Str()
    city = fields.Str()
    state = fields.Str()
    zipcode = fields.Str()