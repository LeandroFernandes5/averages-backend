from app.supplies.schema import SupplySchema
from flask import app, request
from app import app, db
from app.models import Car, Supply
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
   
    return result, 200


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
    
   
    return result, 200


#
#   Post a car
#
@app.post('/cars')
# @token_perms_required(role=['Admin','Supervisor'])
def post_car():

    schema = CarSchema()

    result = schema.load(request.json)

    car = Car(
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

    app.logger.info('Created new Car: %s', request.json)

    return { 'message' : 'Car created' }, 201


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
        
        return result, 200

    return { 'message' : 'Car not found' }, 404


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

        app.logger.info('Updated Car id: %s with %s', carId, request.json)

        return { 'message' : 'Car patched' }, 200

    return { 'message' : 'Car not found' }, 404 


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

        app.logger.info('Activated Car with id:  %s', carId)

        return { 'message' : 'Car Activated' }, 200

    return { 'message' : 'Car not found' }, 404 


#
#   Deactivate Car
#
@app.patch('/cars/<int:carId>/deactivate')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_deact_car(carId):

    car = Car.query.filter_by(id=carId).first()

    if car: 
        
        setattr(car, 'status', 'Inactive')

        db.session.commit()

        app.logger.info('Deactivated Car with id:  %s', carId)

        return { 'message' : 'Car Inactivated' }, 200

    return { 'message' : 'Car not found' }, 404 


#   TODO TBF
#   Get a Car Averages
#
@app.get('/cars/<int:carId>/averages')
# @token_perms_required(role=['Admin','Supervisor'])
def get_car_averages(carId):
    
    car = Car.query.filter_by(id=carId).first()

    if car:
        result =  CarSchema(
            only=('id', 'plate', 'brand', 'model', 'status')
        ).dumps(car)
        
        return result, 200

    return { 'message' : 'Car not found' }, 404


#   
#   Get a Car Supplies 
#
@app.get('/cars/<int:carId>/supplies')
# @token_perms_required(role=['Admin','Supervisor'])
def get_car_supplies(carId):
    
    car = Supply.query.filter_by(carId=carId).all()
    
    if car:
        result =  SupplySchema(many=True,
            only=('id', 'gasStation', 'totalKm', 'liters', 'fullTank', 'cost', 'supplyDate')
        ).dumps(car)
        
        return result, 200

    return { 'message' : 'Car not found' }, 404