from flask import app, request
from app import app, db
from app.models import GasStation
from app.serialization import GasStationSchema
from app.decorators import token_perms_required

#    
#   Get all Supplies
# 
@app.get('/gasstations')
# @token_perms_required(role=['Admin','Supervisor'])
def get_gasstations():

    gas = GasStation.query.all()
    
    result = GasStationSchema(
        many=True,
        only=('id', 'name')
        ).dumps(gas)
    
   
    return result, 200


    #
#   Post a new driver
#
@app.post('/gasstations')
# @token_perms_required(role=['Admin','Supervisor'])
def post_car():

    schema = GasStationSchema()

    result = schema.load(request.json)

    gas = GasStation(
        id = result.get('id'),
        name = result.get('name')
    )

    db.session.add(gas)
    db.session.commit()

    return { 'message' : 'Gas Stations created' }, 201
