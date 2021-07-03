from app import db, ma
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    password = fields.String(load_only=True) # Write only, will never be returned on the JSON output
    name = fields.String()
    role = fields.String() 
    imageURL = fields.String() 
    passwordResetToken = fields.String() 
    status  = fields.String()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)