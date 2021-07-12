from flask import app, request, jsonify
from app import app, db
from app.models import User
from app.users.schema import UserSchema
from app.decorators import token_perms_required

#    
#   Get all users
# 
@app.get('/api/users')
# @token_perms_required(role=['Admin','Supervisor'])
def users():
  
    users = User.query.all()
    result = UserSchema(
        many=True, 
        only=('id', 'email', 'name', )
        ).dumps(users)
    
    return result, 200


#    
#   Register a new user
# 
@app.post('/api/users')
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

    app.logger.info('Created new User for email: %s', email)
    
    return { 'message' : 'User registered' }, 201


#
#   Get a User
#
@app.get('/api/users/<int:userId>')
# @token_perms_required(role=['Admin','Supervisor'])
def get_user(userId):
    
    user = User.query.filter_by(id=userId).first()

    if user:
        result =  UserSchema(
            only=('id', 'email', 'imageURL', 'name', 'status',)
        ).dumps(user)
        
        return result, 200

    return { 'message' : 'User not found' }, 404


#
#   Update a User
#
@app.patch('/api/users/<int:userId>')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_user(userId):

    user = User.query.filter_by(id=userId).first()

    if user: 
        for key, value in request.json.items():
            setattr(User, key, value)

        db.session.commit()

        app.logger.info('Updated User with id:  %s with %s', userId, request.json)

        return { 'message' : 'User updated' }, 200

    return { 'message' : 'User not found' }, 404 



#
#   Change a password
#
@app.put('/api/users/<int:userId>')
# @token_perms_required(role=['Admin','Supervisor'])
def change_password(userId):

    user = User.query.filter_by(id=userId).first()

    if user:

        if user.check_password(request.json.get('oldPassword')):

            user.set_password(request.json.get('password'))

            db.session.add(user)
            db.session.commit()

            app.logger.info('Updated User password - id: %s', userId)

            return {'message' : 'Password changed'}, 200
            
        else: 

            return {'message' : 'Password dont match'}, 404 

    return { 'message' : 'User not found' }, 404       


#
#   Activate User
#
@app.patch('/api/users/<int:userId>/activate')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_user_act(userId):
    
    user = User.query.filter_by(id=userId).first()

    if user:
        setattr(user, 'status', 'Active')

        db.session.commit()

        app.logger.info('Activated User - id: %s', userId)

        return { 'message' : 'User updated' }, 200

    return { 'message' : 'User not found' }, 404


#
#   Update User
#
@app.patch('/api/users/<int:userId>/deactivate')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_user_deact(userId):
    
    user = User.query.filter_by(id=userId).first()

    if user:
        setattr(user, 'status', 'Inactive')

        db.session.commit()

        app.logger.info('Inactivated User - id: %s', userId)

        return { 'message' : 'User updated' }, 200

    return { 'message' : 'User not found' }, 404



#
#   Update Role
#
@app.patch('/api/users/<int:userId>/roles')
# @token_perms_required(role=['Admin','Supervisor'])
def patch_user_roles(userId):
    
    user = User.query.filter_by(id=userId).first()

    role = request.json.get('role')

    if user:
        setattr(user, 'role', role)

        db.session.commit()

        app.logger.info('Role updated User - id: %s', userId)

        return { 'message' : 'Role updated' }, 200

    return { 'message' : 'User not found' }, 404


