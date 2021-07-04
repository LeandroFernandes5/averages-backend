from flask import app, request, jsonify
from app import app, db
from app.models import User
from app.users.schema import UserSchema
import jwt, datetime
from app.decorators import token_perms_required


#    
#   Register a new user
# 
@app.post('/users')
def register():

    email = request.json.get('email')
    
    if User.query.filter_by(email=email).first():
         return jsonify({'message': 'Email already exists' }), 409
    
    user = User(
        email = request.json.get('email'),
        name = request.json.get('name')
    )
    user.set_password(request.json.get('password'))

    db.session.add(user)
    db.session.commit()
    
    return jsonify({ 'message' : 'User registered' }), 201

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

    return jsonify({ 'message' : 'User or password incorrect' }), 401

#    
#   
# 

@app.get('/users')
# @token_perms_required(role=['Admin','Supervisor'])
def users():
  
    users = User.query.all()
    result = UserSchema(
        many=True, 
        only=('id', 'email', 'name', 'role', 'status', )
        ).dumps(users)
    
    return jsonify(result), 200
