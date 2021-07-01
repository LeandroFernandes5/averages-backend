from flask import app, request
from app import app, db
from app.models import Supply
from app.serialization import SupplySchema
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
    
   
    return result, 200

    
#
#   Get a Driver Supplies
#
@app.get('/drivers/<driverId>/supplies')
# @token_perms_required(role=['Admin','Supervisor'])
def get_driver(driverId):
    
    driver = Supply.query.filter_by(id=driverId).first()

    if driver:
        return SupplySchema(
            only=('id', 'name', 'ccNumber', 'driverLicenseNumber', 'driverLicenseExpireDate', 
            'birthDate', 'camExpireDate', 'tccExpireDate', 'ccExpireDate', 'user',)
        ).dumps(driver), 200

    return { 'message' : 'Driver not found' }, 404