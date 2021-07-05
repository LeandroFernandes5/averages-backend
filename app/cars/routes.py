from flask import app, request, jsonify
from app import app, db
from app.models import Car
from app.cars.schema import CarSchema
from app.decorators import token_perms_required

#    
#   Get Cars simplified
# 
@app.get('/cars-simplified')
# @token_perms_required(role=['Admin','Supervisor', 'Driver'])
def get_cars_simplified():

    cars = Car.query.filter_by(status='Active').all()
    
    result = CarSchema(many=True, only=('id', 'plate')).dumps(cars)
   
    return jsonify(result), 200


#    
#   Get Cars
# 
@app.get('/cars')
# @token_perms_required(role=['Admin','Supervisor'])
def get_cars():

    cars = Car.query.all()
    
    result = CarSchema(
        many=True,
        only=('id', 'plate', 'brand', 'model', 'registerDate', 
        'chassisNo', 'obraNo', 'inspectionDate', 'tccExpireDate',
        'licenseExpireDate', 'tachographDate')
        ).dumps(cars)
    
   
    return jsonify(result), 200


#
#   Post a car
#
@app.post('/cars')
# @token_perms_required(role=['Admin','Supervisor'])
def post_car():

    schema = CarSchema()

    result = schema.load(request.json)

    car = Car(
        id = result.get('id'),
        plate = result.get('plate'),
        brand = result.get('brand'),
        model = result.get('model'),
        registerDate = result.get('registerDate'),
        status = result.get('status'),
        chassisNo = result.get('chassisNo'),
        obraNo = result.get('obraNo'),
        inspectionDate = result.get('inspectionDate'),
        tccExpireDate = result.get('tccExpireDate'),
        licenseExpireDate = result.get('licenseExpireDate'),
        tachographDate = result.get('tachographDate')
    )

    db.session.add(car)
    db.session.commit()

    return jsonify({ 'message' : 'Car created' }), 201


#
#   Get a Car
#
@app.get('/cars/<int:carId>')
# @token_perms_required(role=['Admin','Supervisor'])
def get_car(carId):
    
    car = Car.query.filter_by(id=carId).first()

    if car:
        result =  CarSchema(
            only=('id', 'plate', 'model', 'registerDate', 'chassisNo', 
            'obraNo', 'inspectionDate', 'tccExpireDate', 'licenseExpireDate', 'tachographDate', 'status')
        ).dumps(car)
        
        return jsonify(result), 200

    return jsonify({ 'message' : 'Car not found' }), 404


#
#   Delete a Car
#
@app.delete('/cars/<int:carId>')
# @token_perms_required(role=['Admin','Supervisor'])
def del_car(carId):
    
    car = Car.query.filter_by(id=carId).first()

    if car:
        db.session.delete(car)
        db.session.commit()

        return jsonify({ 'message' : 'Car deleted' }), 200

    return jsonify({ 'message' : 'Car not found' }), 404


#
#   Update a car
#
@app.patch('/cars/<int:carId>')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_car(carId):

    car = Car.query.filter_by(id=carId).first()

    if car: 
        for key, value in request.json.items():
            setattr(car, key, value)

        db.session.commit()

        return jsonify({ 'message' : 'Car patched' }), 200

    return jsonify({ 'message' : 'Car not found' }), 404 


#
#   Activate Car
#
@app.patch('/cars/<int:carId>/activate')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_act_car(carId):

    car = Car.query.filter_by(id=carId).first()

    if car: 

        setattr(car, 'status', 'Active')

        db.session.commit()

        return jsonify({ 'message' : 'Car Activated' }), 200

    return jsonify({ 'message' : 'Car not found' }), 404 


#
#   Activate Car
#
@app.patch('/cars/<int:carId>/deactivate')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_deact_car(carId):

    car = Car.query.filter_by(id=carId).first()

    if car: 
        
        setattr(car, 'status', 'Inactive')

        db.session.commit()

        return jsonify({ 'message' : 'Car Inactivated' }), 200

    return jsonify({ 'message' : 'Car not found' }), 404 
