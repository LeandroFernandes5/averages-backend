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

class DriverSchema(Schema):
    id = fields.Int()
    name = fields.String()
    birthDate = fields.DateTime()
    ccNumber = fields.String()
    ccExpireDate = fields.DateTime()
    driverLicenseNumber = fields.String() 
    driverLicenseExpireDate = fields.String() 
    tccExpireDate  = fields.DateTime()
    camExpireDate = fields.DateTime() 
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)
    user = fields.Nested(UserSchema(only=("email",)))