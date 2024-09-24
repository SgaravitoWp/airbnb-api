from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.String(required=True,
                             validate=validate.Length(max=100)  )
    password = fields.String(required=True,
                             validate=validate.Length(max=100) )
