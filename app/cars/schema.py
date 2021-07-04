from app import db, ma
from marshmallow import Schema, fields

class CarSchema(Schema):
    id = fields.Int()
    plate = fields.String()
    brand = fields.String()
    model = fields.String()
    registerDate = fields.DateTime()
    chassisNo = fields.String() 
    obraNo = fields.String() 
    inspectionDate  = fields.DateTime()
    tccExpireDate = fields.DateTime() 
    licenseExpireDate = fields.DateTime()
    tachographDate = fields.DateTime()
    status = fields.String()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)