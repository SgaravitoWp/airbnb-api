from schemas.password_check import check_password_strength
from marshmallow import ValidationError
from marshmallow import Schema, fields
from models.tables import *
import re 


class UserSchema(Schema):
    user_id = fields.String(dump_only=True)
    username = fields.String(load_only=True)
    password = fields.String(load_only=True)

class UserSignUpSchema(UserSchema):
    
    @staticmethod
    def validate_username(username):
        errors = []
        if not (3 <= len(username) <= 20):
            errors.append("The username length is not within the required range.")
        else:
            if not (bool(re.match(r'^[A-Za-z0-9_-]+$', username))):
                errors.append("The username cannot contain special characters.")

        if errors: 
            return {"username": errors}
        else:
            return dict()

    @staticmethod
    def validate_password(username, password):
        errors = []
        if not (3 <= len(password) <= 50):
            errors.append("The password length is not within the required range.")
        else:
            password_feedback = check_password_strength(password=password, 
                                                        user_inputs=[username])
            if password_feedback:
                errors += password_feedback
            if not (bool(re.match(r'^[A-Za-z0-9_\-!@$%^&*+#.]+$', password))):
                errors.append("The password cannot contain special characters.")

        if errors: 
            return {"password": errors}
        else:
            return dict()
    
    def load(self, *args, **kwargs):
        data = super().load(*args, **kwargs)
        errors = dict()
        errors = {**errors, **self.validate_username(data['username'])}
        errors = {**errors, **self.validate_password(data['username'], data["password"])}
        
        if errors:
            raise ValidationError(errors)  
        return data

class SignUpErrorSchema(Schema):

    password = fields.List(fields.Str(), required=False)
    username = fields.List(fields.Str(), required=False)

class ResponseSchema(Schema):
    success = fields.Bool(required=True)
    message = fields.String(required=True)
    status_code = fields.Integer(required=True)


class TokenSchema(Schema):
    token = fields.String(required=True)

class Message(Schema):

    error_type = fields.List(fields.Str(), required=False) 

def define_response(name, data_object):
    class NewClass(ResponseSchema):
        
        data = fields.Nested(data_object, required = False)


    NewClass.__name__ = name  
    return NewClass