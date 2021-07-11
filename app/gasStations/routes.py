from flask import app, request, jsonify
from app import app, db
from app.models import GasStation
from app.gasStations.schema import GasStationSchema
from app.decorators import token_perms_required

#    
#   Get all Gas Stations
# 
@app.get('/api/gasstations')
# @token_perms_required(role=['Admin','Supervisor'])
def get_gasstations():

    gas = GasStation.query.all()
    
    result = GasStationSchema(
        many=True,
        only=('id', 'name')
        ).dumps(gas)
    
   
    return result, 200


#
#   Post a new Gas Station
#
@app.post('/api/gasstations')
# @token_perms_required(role=['Admin','Supervisor'])
def post_gasstations():

    schema = GasStationSchema()

    result = schema.load(request.json)

    gas = GasStation(
        id = result.get('/apiid'),
        name = result.get('/apiname')
    )

    db.session.add(gas)
    db.session.commit()

    app.logger.info('Created new Gas Station: %s', request.json)

    return { 'message' : 'Gas Station created' }, 201


#
#   Delete Gas Station
#
@app.delete('/gasstations/<int:gasStationId>')
# @token_perms_required(role=['Admin','Supervisor'])
def del_gasstation(gasStationId):
    
    gas = GasStation.query.filter_by(id=gasStationId).first()

    if gas:
        db.session.delete(gas)
        db.session.commit()

        app.logger.info('Deleted Gas Station id: %s', gasStationId)

        return { 'message' : 'Gas Station deleted' }, 200

    return { 'message' : 'Gas Station not found' }, 404


#
#   Update Gas Station
#
@app.patch('/api/gasstations/<int:gasStationId>')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_gasstation(gasStationId):
    
    gas = GasStation.query.filter_by(id=gasStationId).first()

    if gas:
        for key, value in request.json.items():
            setattr(gas, key, value)

        db.session.commit()

        app.logger.info('Updated Gas Station id: %s with %s', gasStationId, request.json)

        return { 'message' : 'Gas Station updated' }, 200

    return { 'message' : 'Gas Station not found' }, 404