from flask import app, request
from app import app, db
from app.models import Driver
from app.serialization import DriverSchema
from app.decorators import token_perms_required


#
#   Post a new driver
#
@app.post('/drivers')
# @token_perms_required(role=['Admin','Supervisor'])
def post_driver():

    schema = DriverSchema()

    result = schema.load(request.json)

    # driver = Driver(result)
    driver = Driver(
        id = result.get('id'),
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

    return { 'message' : 'Driver created' }, 201


#    
#   Get all Drivers
# 
@app.get('/drivers')
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
#   Get Driver
#
@app.get('/drivers/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def get_driver(id):
    
    driver = Driver.query.filter_by(id=id).first()

    if driver:
        return DriverSchema(
            only=('id', 'name', 'ccNumber', 'driverLicenseNumber', 'driverLicenseExpireDate', 
            'birthDate', 'camExpireDate', 'tccExpireDate', 'ccExpireDate', 'user',)
        ).dumps(driver), 200

    return { 'message' : 'Driver not found' }, 404


#
#   Delete Driver
#
@app.delete('/drivers/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def del_driver(id):
    
    driver = Driver.query.filter_by(id=id).first()

    if driver:
        db.session.delete(driver)
        db.session.commit()

        return { 'message' : 'Driver deleted' }, 200

    return { 'message' : 'Driver not found' }, 404