from flask import app, request
from app import app, db
from app.models import Car
from app.cars.schema import CarSchema
from app.decorators import token_perms_required

#    
#   Get a Cars
# 
@app.get('/cars')
# @token_perms_required(role=['Admin','Supervisor'])
def get_cars():

    cars = Car.query.all()
    
    result = CarSchema(
        many=True,
        only=('id', 'plate', 'brand', 'model', 'registerDate', 
        'chassisNo', 'obraNo', 'inspectionDate', 'tccExpireDate',
        'licenseDate', 'tachographDate')
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
        id = result.get('id'),
        plate = result.get('plate'),
        brand = result.get('brand'),
        model = result.get('model'),
        registerDate = result.get('registerDate'),
        chassisNo = result.get('chassisNo'),
        obraNo = result.get('obraNo'),
        inspectionDate = result.get('inspectionDate'),
        tccExpireDate = result.get('tccExpireDate'),
        licenseDate = result.get('licenseDate'),
        tachographDate = result.get('tachographDate'),
        userId = result.get('userId')
    )

    db.session.add(car)
    db.session.commit()

    return { 'message' : 'Car created' }, 201


#
#   Get a Car
#
@app.get('/cars/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def get_car(id):
    
    car = Car.query.filter_by(id=id).first()

    if car:
        return CarSchema(
            only=('id', 'plate', 'model', 'registerDate', 'chassisNo', 
            'obraNo', 'inspectionDate', 'tccExpireDate', 'licenseDate', 'tachographDate',)
        ).dumps(car), 200

    return { 'message' : 'Car not found' }, 404


#
#   Delete a Car
#
@app.delete('/cars/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def del_car(id):
    
    car = Car.query.filter_by(id=id).first()

    if car:
        db.session.delete(car)
        db.session.commit()

        return { 'message' : 'Car deleted' }, 200

    return { 'message' : 'Car not found' }, 404


#
#   Update a car
#
@app.put('/cars/<int:id>')
# @token_perms_required(role=['Admin','Supervisor'])
def put_car(id):

    car = Car.query.filter_by(id=id).first()

    if car: 
        for key, value in request.json.items():
            setattr(car, key, value)

        db.session.commit()

        return { 'message' : 'Car created' }, 200

    return { 'message' : 'Car not found' }, 404 
