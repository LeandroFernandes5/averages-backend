from flask import app, request
from flask.json import jsonify
from app import app, db
from app.models import User
from pprint import pprint
import jwt 
import datetime


#    
#   Register a new user
# 
@app.post('/register')
def register():

    email = request.json.get('email')
    
    if User.query.filter_by(email=email).first():
         return jsonify({'message': 'User already exists' }), 401
    
    user = User(
        email = request.json.get('email'),
        first_name = request.json.get('first_name'),
        last_name = request.json.get('last_name')
    )
    user.set_password(request.json.get('password'))

    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered!' }), 200


@app.post('/login')
def login():
    
    user = User.query.filter_by(email=request.json.get('email')).first()

    if user and user.check_password(request.json.get('password')):
        payload = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            # 'role': user.role,
            # 'status': user.status,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'])
        
        return jsonify({'token': token}), 200

    return jsonify({'message': 'testing phase'}), 401

@app.get('/users')
def users():

    users = User.query.all()
    return jsonify(users), 200