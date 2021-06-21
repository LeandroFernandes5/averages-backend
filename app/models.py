from sqlalchemy.orm import relationship
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.sql import func
from enum import Enum
# from dataclasses import dataclass

# class AccountStatus(Enum):
#     Active = 'Active' #Pode fazer tudo
#     Pending = 'Pending' # Pendente de confirmation por admin
#     Inactive = 'Inactive' #Conta foi apagada/desativada por um admin

# class Role(db.Model):
   
    # Admin = 'Admin'
    # Coordinator = 'Coordinator'
    # Driver = 'Driver'
    # Watcher = 'Watcher'

# @dataclass
class User(db.Model):
 
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(128), index=True, unique=True, nullable=False)
    password = db.Column('password', db.String(128), nullable=False, unique=False)
    name = db.Column('name', db.String(64), nullable=False, unique=False)
    role = db.Column('role', db.String(64), nullable=False, unique=False, server_default='Driver')
    image = db.Column('image', db.String(128), nullable=True, unique=False)
    password_reset_token = db.Column('password_reset_token', db.String(128), nullable=True,  unique=False)
    status = db.Column('status', db.String(64), nullable=False, unique=False, server_default='Pending')
    created_date = db.Column('created_date', db.DateTime, nullable=False,  unique=False, server_default=func.now())
    modified_date = db.Column('modified_date', db.DateTime, nullable=True,  unique=False, onupdate=func.now())

    #
    # @password.setter
    #
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return '<User {}>'.format(self.email)    