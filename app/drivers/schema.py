from app import db, ma
from marshmallow import Schema, fields
from app.users.schema import UserSchema

class DriverSchema(Schema):
    id = fields.Int()
    imageURL = fields.String() 
    name = fields.String()
    birthDate = fields.DateTime()
    ccNumber = fields.String()
    ccExpireDate = fields.DateTime()
    driverLicenseNumber = fields.String() 
    driverLicenseExpireDate = fields.DateTime() 
    tccExpireDate  = fields.DateTime()
    camExpireDate = fields.DateTime() 
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)
    user = fields.Nested(UserSchema(only=("id","email","name","status","role")))