from flask import app, request
from flask.json import jsonify
from app import app, db, ma
from app.models import User, Driver, driver_schema, drivers_schema
from app.decorators import token_perms_required



#
#   Post a new driver
#
@app.post('/drivers')
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
        user_id = request.json.get('user_id')
    )

    db.session.add(driver)
    db.session.commit()

    return driver_schema.jsonify(driver), 201


#    
#   Get all Drivers
# 
@app.get('/drivers')
@token_perms_required(role=['Admin','Supervisor'])
def get_drivers():

    drivers = Driver.query.all()
    result = drivers_schema.dump(drivers)
   
    return jsonify(result), 200

    
#
#   Get Driver
#
@app.get('/drivers/<id>')
def get_driver(id):
    
    driver = Driver.query.get(id)

    if driver:
        return driver_schema.dump(driver), 200

    return {'message': 'Driver not found!' }, 404