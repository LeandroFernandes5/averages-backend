from app import db, ma
from marshmallow import Schema, fields

class GasStationSchema(Schema):
    id = fields.Int()
    name = fields.String()
    createdDate = fields.DateTime(load_only=True)
    modifiedDate = fields.DateTime(load_only=True)