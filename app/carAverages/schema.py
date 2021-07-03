from app import db, ma
from marshmallow import Schema, fields
from app.cars.schema import CarSchema

class CarAveragesSchema(Schema):
    id = fields.Int()
    liters = fields.Float()
    km = fields.Integer()
    year = fields.Integer()
    month = fields.Integer()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)
    car = fields.Nested(CarSchema(only=("id","plate",)))