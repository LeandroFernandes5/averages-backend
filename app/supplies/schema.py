from sqlalchemy.orm import load_only
from app import db, ma
from marshmallow import Schema, fields
from app.cars.schema import CarSchema
from app.gasStations.schema import GasStationSchema
from app.drivers.schema import DriverSchema

class SupplySchema(Schema):
    id = fields.Int()
    totalKm = fields.Int()
    liters = fields.Float()
    fullTank = fields.Boolean()
    cost = fields.Float()
    supplyDate = fields.DateTime()
    average = fields.Float()
    isSupplyPast = fields.Boolean()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)
    gasStationId = fields.Int(load_only=True)
    gasStation = fields.Nested(GasStationSchema(only=("id","name",)))
    driverId = fields.Int()
    driver = fields.Nested(DriverSchema(only=("id","name","ccNumber")))
    carId = fields.Int()
    car = fields.Nested(CarSchema(only=("id","plate",)))