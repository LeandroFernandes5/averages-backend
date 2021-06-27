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

    driver = Driver(
        name = request.json.get('name'),
        image = request.json.get('image'),
        birthDate = request.json.get('birthDate'),
        ccNumber = request.json.get('ccNumber'),
        ccExpireDate = request.json.get('ccExpireDate'),
        driverLicenseNumber = request.json.get('driverLicenseNumber'),
        driverLicenseExpireDate = request.json.get('driverLicenseExpireDate'),
        tccExpireDate = request.json.get('tccExpireDate'),
        camExpireDate = request.json.get('camExpireDate'),
        userId = request.json.get('userId')
    )

    db.session.add(driver)
    db.session.commit()

    return { 'message' : 'Driver created!' }, 201


#    
#   Get all Drivers
# 
@app.get('/drivers')
# @token_perms_required(role=['Admin','Supervisor'])
def get_drivers():

    drivers = Driver.query.all()
    
    result = DriverSchema(
        many=True,
        only=('id', 'name', 'ccNumber', 'driverLicenseNumber', 'driverLicenseExpireDate', 'birthDate', 'camExpireDate', 'user', 'tccExpireDate', 'ccExpireDate')
        ).dumps(drivers)
    
   
    return result, 200

    
#
#   Get Driver
#
@app.get('/drivers/<id>')
# @token_perms_required(role=['Admin','Supervisor'])
def get_driver(id):
    
    driver = Driver.query.filter_by(id=id).first()

    if driver:
        return DriverSchema().dumps(driver), 200

    return { 'message' : 'Driver not found!' }, 404