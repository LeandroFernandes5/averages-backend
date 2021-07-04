from flask import app, jsonify
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

    supplies = Supply.query.all()
    
    result = SupplySchema(
        many=True,
        only=('id', 'totalKm', 'liters', 'fullTank', 'cost', 
        'supplyDate', 'average', 'gasStation', 
        'driver', 'car')
        ).dumps(supplies)
    
   
    return jsonify(result), 200

    
#
#   Get a Driver Supplies
#
@app.get('/drivers/<int:driverId>/supplies')
# @token_perms_required(role=['Admin','Supervisor'])
def get_driver_supplies(driverId):
    
    driver = Supply.query.filter_by(id=driverId).first()

    if driver:
        result = SupplySchema(
            only=('id', 'name', 'ccNumber', 'driverLicenseNumber', 'driverLicenseExpireDate', 
            'birthDate', 'camExpireDate', 'tccExpireDate', 'ccExpireDate', 'user',)
        ).dumps(driver)
        
        return jsonify(result), 200

    return jsonify({ 'message' : 'Driver not found' }), 404


#
#   Delete Supply
#
@app.delete('/supplies/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def supplies_driver(id):
    
    supply = Supply.query.filter_by(id=id).first()

    if supply:
        db.session.delete(supply)
        db.session.commit()

        return jsonify({ 'message' : 'Supply deleted' }), 200

    return jsonify({ 'message' : 'Supply not found' }), 404