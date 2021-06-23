from flask import app, request
from flask.json import jsonify
from app import app, db
from app.models import User
import jwt 
from functools import wraps


def token_perms_required(role):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):

            token = None

            if 'Authorization' in request.headers:
               token = request.headers['Authorization']

            if not token:
               return {'message': 'Token not found'}, 401

            try:
               data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=app.config['ALGORITHM'])

               if not data['role'] in role:
                  return jsonify({'message': 'Forbidden'}), 403

            except:

               return jsonify({'message': 'Token not valid'}), 403
            
            return f(*args, **kwargs)
        return wrapped
    return inner_decorator

