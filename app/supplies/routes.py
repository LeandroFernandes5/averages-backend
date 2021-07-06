from flask import app, jsonify, request
from app import app, db
from app.models import Supply
from app.supplies.schema import SupplySchema
from app.decorators import token_perms_required

#    
#   Get all Supplies
# 
@app.get('/supplies')
# @token_perms_required(role=['Admin','Supervisor'])
def get_supplies():

    sups = Supply.query.all()
    
    result = SupplySchema(
        many=True,
        only=('id', 'totalKm', 'liters', 'fullTank', 'cost', 
        'supplyDate', 'average', 'gasStation', 
        'driver', 'car')
        ).dumps(sups)
    
   
    return result, 200


#
#   Post a new supply
#
@app.post('/supplies')
# @token_perms_required(role=['Admin','Supervisor'])
def post_supplies():

    schema = SupplySchema()

    result = schema.load(request.json)

    supply = Supply(
        driverId = result.get('driverId'),
        carId = result.get('carId'),
        gasStationId = result.get('gasStationId'),
        totalKm = result.get('totalKm'),
        liters = result.get('liters'),
        fullTank = result.get('fullTank'),
        supplyDate = result.get('supplyDate'),
        cost = result.get('cost')
    )

    supply.average = 0
    # 
    # TODO: Add proper average calculation 
    #  

    db.session.add(supply)
    db.session.commit()

    return { 'message' : 'Supply created' }, 201


#
#   Get Supply
#
@app.get('/supplies/<int:supplyId>')
# @token_perms_required(role=['Admin','Supervisor'])
def get_supply(supplyId):
    
    sup = Supply.query.filter_by(id=supplyId).first()

    if sup:
        result = SupplySchema(
            only=('id', 'totalKm', 'liters', 'fullTank', 'cost', 
            'supplyDate', 'average', 'driver', 'car','gasStation', )
        ).dumps(sup)

        return result, 200

    return { 'message' : 'Supply not found' }, 404


#
#   Update a Supply
#
@app.patch('/supplies/<int:supplyId>')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_supplies(supplyId):

    sup = Supply.query.filter_by(id=supplyId).first()
    
    if sup:
        for key, value in request.json.items():
            setattr(sup, key, value)

        db.session.commit()

        ## TODO Add average calculation

        return { 'message' : 'Supply updated' }, 200
    
    return { 'message' : 'Supply not found' }, 404 


#
#   Delete Supply
#
@app.delete('/supplies/<int:supplyId>')
# @token_perms_required(role=['Admin','Supervisor'])
def del_supplies(id):
    
    supply = Supply.query.filter_by(id=id).first()

    if supply:
        db.session.delete(supply)
        db.session.commit()

        ### TODO Add average calculation

        return { 'message' : 'Supply deleted' }, 200

    return { 'message' : 'Supply not found' }, 404