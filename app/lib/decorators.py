from flask import app, request
from app import app, db
import jwt 


def token_perms_required(role):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):

            token = None

            if 'Authorization' in request.headers:
               token = request.headers['Authorization']

            if not token:
               return {'message': 'Token not found.'}, 401

            try:
               data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=app.config['ALGORITHM'])

               if not data['role'] in role:
                  return {'message': 'No permissions.'}, 403

            except:

               return {'message': 'Bad request.'}, 400
            
            return f(*args, **kwargs)
        return wrapped
    return inner_decorator

