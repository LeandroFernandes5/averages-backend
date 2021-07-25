from flask import app, request, jsonify
from app import app, db
from app.models import Driver, Supply
from app.drivers.schema import DriverSchema, DriverSimplifiedSchema
from app.supplies.schema import SupplySchema
from app.lib.decorators import token_perms_required

#
#   Get Driver Simplified
#
@app.get('/api/drivers-simplified')
# @token_perms_required(role=['Admin','Supervisor'])
def driver_simplified():
    
    driver = Driver.query.all()

    print(driver)

    if driver:
        result = DriverSimplifiedSchema(
            many=True,
            only=('id', 'name', 'user')
        ).dumps(driver)

        return result, 200

    return { 'message' : 'Driver not found' }, 404


#    
#   Get all Drivers
# 
@app.get('/api/drivers')
# @token_perms_required(role=['Admin','Supervisor'])
def get_drivers():

    drivers = Driver.query.all()
    
    result = DriverSchema(
        many=True,
        only=('id', 'name', 'ccNumber', 'driverLicenseNumber', 'driverLicenseExpireDate', 
        'birthDate', 'camExpireDate', 'tccExpireDate', 'ccExpireDate')
        ).dumps(drivers)
    
   
    return result, 200


#
#   Post a new driver
#
@app.post('/api/drivers')
# @token_perms_required(role=['Admin','Supervisor'])
def post_driver():

    schema = DriverSchema()

    result = schema.load(request.json)

    driver = Driver(
        name = result.get('name'),
        imageURL = result.get('imageURL'),
        birthDate = result.get('birthDate'),
        ccNumber = result.get('ccNumber'),
        ccExpireDate = result.get('ccExpireDate'),
        driverLicenseNumber = result.get('driverLicenseNumber'),
        driverLicenseExpireDate = result.get('driverLicenseExpireDate'),
        tccExpireDate = result.get('tccExpireDate'),
        camExpireDate = result.get('camExpireDate'),
        userId = result.get('userId')
    )

    db.session.add(driver)
    db.session.commit()

    app.logger.info('Created new Driver :  %s', request.json)

    return { 'message' : 'Driver created' }, 201


    
#
#   Get Driver
#
@app.get('/api/drivers/<int:driverId>')
# @token_perms_required(role=['Admin','Supervisor'])
def get_driver(driverId):
    
    driver = Driver.query.filter_by(id=driverId).first()

    if driver:
        result = DriverSchema(
            only=('id', 'name', 'ccNumber', 'driverLicenseNumber', 'driverLicenseExpireDate', 
            'birthDate', 'camExpireDate', 'tccExpireDate', 'ccExpireDate',)
        ).dumps(driver)

        return result, 200

    return { 'message' : 'Driver not found' }, 404



#
#   Update a driver
#
@app.patch('/api/drivers/<int:driverId>')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_driver(driverId):

    driver = Driver.query.filter_by(id=driverId).first()
    
    if driver:
        for key, value in request.json.items():
            setattr(driver, key, value)

        db.session.commit()

        app.logger.info('Updated Driver id: %s with ', driverId, request.json)

        return { 'message' : 'Driver updated' }, 200
    
    return { 'message' : 'Driver not found' }, 404 



#
#   Get a Driver Supplies
#
@app.get('/api/drivers/<int:driverId>/supplies')
# @token_perms_required(role=['Admin','Supervisor'])
def get_driver_supplies(driverId):
    
    driver = Supply.query.filter_by(id=driverId).first()

    if driver:
        result = SupplySchema(
            only=('id', 'name', 'ccNumber', 'driverLicenseNumber', 'driverLicenseExpireDate', 
            'birthDate', 'camExpireDate', 'tccExpireDate', 'ccExpireDate', 'user',)
        ).dumps(driver)
        
        return result, 200

    return { 'message' : 'Driver not found' }, 404


