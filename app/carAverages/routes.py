from flask import app, request
from app import app, db
from app.models import CarAverage
from app.carAverages.schema import CarAveragesSchema
from app.decorators import token_perms_required

#    
#   Get all Supplies
# 
@app.get('/caraverages')
# @token_perms_required(role=['Admin','Supervisor'])
def get_caraverages():

    avg = CarAverage.query.all()
    
    result = CarAveragesSchema(
        many=True,
        only=('id', 'liters', 'km', 'year', 'month', 'car')
        ).dumps(avg)
    
   
    return result, 200

    