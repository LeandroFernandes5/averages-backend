from flask import app, request, jsonify
from app import app, db
from app.models import User
from app.users.schema import UserSchema
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
#   Get all users
# 
@app.get('/users')
# @token_perms_required(role=['Admin','Supervisor'])
def users():
  
    users = User.query.all()
    result = UserSchema(
        many=True, 
        only=('id', 'email', 'name', )
        ).dumps(users)
    
    return jsonify(result), 200


#
#   Update User
#
@app.patch('/users/<int:userId>/activate')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_user_act(userId):
    
    user = User.query.filter_by(id=userId).first()

    if user:
        setattr(user, 'status', 'Active')

        db.session.commit()

        return jsonify({ 'message' : 'User updated' }), 200

    return jsonify({ 'message' : 'User not found' }), 404


#
#   Update User
#
@app.patch('/users/<int:userId>/deactivate')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_user_act(userId):
    
    user = User.query.filter_by(id=userId).first()

    if user:
        setattr(user, 'status', 'Inactive')

        db.session.commit()

        return jsonify({ 'message' : 'User updated' }), 200

    return jsonify({ 'message' : 'User not found' }), 404