from flask import app, jsonify, request
from app import app, db
from app.models import Supply
from app.supplies.schema import SupplySchema
from app.lib.decorators import token_perms_required
from app.lib.businessLogic import *
import datetime

#    
#   Get all Supplies
# 
@app.get('/api/supplies')
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
@app.post('/api/supplies')
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
    
    supply.average = averageCalculation(supply) 

    if result.get('supplyDate').date() != datetime.date.today():
        supply.isSupplyPast = True

    db.session.add(supply)
    db.session.commit()

    app.logger.info('Created new Supply %s ', request.json)

    averageMonthlyCalculation(supply)

    return { 'message' : 'Supply created' }, 201


#
#   Get Supply
#
@app.get('/api/supplies/<int:supplyId>')
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
@app.patch('/api/supplies/<int:supplyId>')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_supplies(supplyId):

    sup = Supply.query.filter_by(id=supplyId).first()
    
    if sup:
        for key, value in request.json.items():
            setattr(sup, key, value)

        db.session.commit()

        ## TODO Add average calculation
        app.logger.info('Updated Supply id: %s with %s', supplyId, request.json)
        
        return { 'message' : 'Supply updated' }, 200
    
    return { 'message' : 'Supply not found' }, 404 


#
#   Delete Supply
#
@app.delete('/api/supplies/<int:supplyId>')
# @token_perms_required(role=['Admin','Supervisor'])
def del_supplies(supplyId):
    
    supply = Supply.query.filter_by(id=supplyId).first()

    if supply:
        db.session.delete(supply)
        db.session.commit()

        delAverage(supply)

        app.logger.info('Deleted Supply with id:  %s', supplyId)

        return { 'message' : 'Supply deleted' }, 200

    return { 'message' : 'Supply not found' }, 404