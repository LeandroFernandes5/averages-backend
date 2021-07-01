from flask import app, request
from app import app, db
from app.models import Car
from app.serialization import CarSchema
from app.decorators import token_perms_required

#    
#   Get all Supplies
# 
@app.get('/car')
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
#   Post a new driver
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
