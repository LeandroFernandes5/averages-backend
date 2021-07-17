from app import db, ma
from marshmallow import Schema, fields
from app.cars.schema import CarSchema

class CarAveragesSchema(Schema):
    id = fields.Int()
    liters = fields.Float()
    km = fields.Integer()
    year = fields.Integer()
    month = fields.Integer()
    average = fields.Float()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)
    carId = fields.Int(load_only=True)
    car = fields.Nested(CarSchema(only=("id","plate", "brand", "model", "status",)))