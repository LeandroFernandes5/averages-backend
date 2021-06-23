from flask import app, request
from flask.json import jsonify
from app import app, db
from app.models import User, Driver
from pprint import pprint
import jwt 
import datetime


#    
#   Register a new user
# 
@app.post('/users')
def register():

    email = request.json.get('email')
    
    if User.query.filter_by(email=email).first():
         return jsonify({'message': 'User already exists' }), 401
    
    user = User(
        email = request.json.get('email'),
        name = request.json.get('name')
    )
    user.set_password(request.json.get('password'))

    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered!' }), 201

#    
#   Login
# 
@app.post('/me/login')
def login():
    
    
    user = User.query.filter_by(email=request.json.get('email')).first()
    
    if user and user.check_password(request.json.get('password')):
        payload = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'status': user.status,
            'exp' : datetime.datetime.now() + datetime.timedelta(minutes=app.config['TOKEN_TIME_MIN'])
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm=app.config['ALGORITHM'])
        
        return jsonify({'accessToken': token}), 201

    return jsonify({'message': 'No User has that email'}), 401

#    
#   
# 
@app.get('/users')
def users():

    # users = User.query.all()
    # pprint(users)
    # result = user_schema.dumps(users)
    # pprint(result)
    # response = {
    #         'data': result,
    #         'status_code' : 202
    # }
    # pprint(users_schema.dump(User.query.all()))
    # pprint(user_schema.dump(User.query.all()))
    # pprint(User.query.all())


    return {'coisas': 'leo'}