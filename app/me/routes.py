from flask import app, request, jsonify
from app import app, db
from app.models import User
from app.users.schema import UserSchema
import jwt, datetime
from app.decorators import token_perms_required


#    
#   Login
# 
@app.post('/me/login')
def login():
    
    
    user = User.query.filter_by(email=request.json.get('email')).first()

    if user and user.check_password(request.json.get('password')):
        if user.status == 'Active':
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
        else:
            return jsonify({'message' : 'Not authorized'}), 401

    return jsonify({ 'message' : 'User or password incorrect' }), 400
