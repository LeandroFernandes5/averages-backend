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
    user = fields.Nested(UserSchema(only=("id","email","name","status","role")))


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
    licenseDate = fields.DateTime()
    tachographDate = fields.DateTime()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)


class CarAveragesSchema(Schema):
    id = fields.Int()
    liters = fields.Float()
    km = fields.Integer()
    year = fields.Integer()
    month = fields.Integer()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)
    car = fields.Nested(CarSchema(only=("id","plate",)))


class GasStationSchema(Schema):
    id = fields.Int()
    name = fields.String()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)


class SupplySchema(Schema):
    id = fields.Int()
    totalKm = fields.String()
    liters = fields.Float()
    fullTank = fields.Boolean()
    cost = fields.Float()
    supplyDate = fields.DateTime()
    average = fields.Float()
    gasStation = fields.Nested(GasStationSchema(only=("id","name",)))
    driver = fields.Nested(DriverSchema(only=("id","name","ccNumber")))
    car = fields.Nested(CarSchema(only=("id","plate",)))
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)
