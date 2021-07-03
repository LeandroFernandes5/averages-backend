from app import db, ma
from marshmallow import Schema, fields
from app.cars.schema import CarSchema
from app.gasStations.schema import GasStationSchema
from app.drivers.schema import DriverSchema

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