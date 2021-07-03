from flask import app, request
from app import app, db
from app.models import GasStation
from app.gasStations.schema import GasStationSchema
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
def post_gasstations():

    schema = GasStationSchema()

    result = schema.load(request.json)

    gas = GasStation(
        id = result.get('id'),
        name = result.get('name')
    )

    db.session.add(gas)
    db.session.commit()

    return { 'message' : 'Gas Station created' }, 201


#
#   Delete Gas Station
#
@app.delete('/gasstations/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def del_gasstation(id):
    
    gas = GasStation.query.filter_by(id=id).first()

    if gas:
        db.session.delete(gas)
        db.session.commit()

        return { 'message' : 'Gas Station deleted' }, 200

    return { 'message' : 'Gas Station not found' }, 404


#
#   Update Gas Station
#
@app.put('/gasstations/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def put_gasstation(id):
    
    gas = GasStation.query.filter_by(id=id).first()

    if gas:
        for key, value in request.json.items():
            setattr(gas, key, value)

        db.session.commit()

        return { 'message' : 'Gas Station updated' }, 200

    return { 'message' : 'Gas Station not found' }, 404