from datetime import date
from sqlalchemy.orm import relationship
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.sql import func
import datetime


class User(db.Model):
 
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(128), index=True, unique=True, nullable=False)
    password = db.Column('password', db.String(128), nullable=False, unique=False)
    name = db.Column('name', db.String(64), nullable=False, unique=False)
    role = db.Column('role', db.String(64), nullable=False, unique=False, server_default='Driver')
    imageURL = db.Column('image', db.String(128), nullable=True, unique=False)
    passwordResetToken = db.Column('password_reset_token', db.String(128), nullable=True,  unique=False)
    status = db.Column('status', db.String(64), nullable=False, unique=False, server_default='Pending')
    createdDate = db.Column('createdDate', db.DateTime, nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime, nullable=True,  unique=False, onupdate=func.now())
    driver = relationship("Driver", uselist=False, backref="user")

    #
    # @password.setter
    #
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return '<User {}>'.format(self.email)    


class Driver(db.Model):

    __tablename__ = 'drivers'

    id = db.Column('id', db.Integer, primary_key=True)
    image = db.Column('image', db.String(128), nullable=True, unique=False)
    name = db.Column('name', db.String(64), nullable=False, unique=False)
    birthDate = db.Column('birth_date', db.DateTime, nullable=True, unique=False)
    ccNumber = db.Column('cc_number', db.String(64), nullable=True, unique=False)
    ccExpireDate = db.Column('cc_expire_date', db.DateTime, nullable=True, unique=False)
    driverLicenseNumber = db.Column('driver_license_number', db.String(64), nullable=True, unique=False)
    driverLicenseExpireDate = db.Column('driver_license_expire_date', db.DateTime, nullable=True, unique=False)
    tccExpireDate = db.Column('tcc_expire_date', db.DateTime, nullable=True, unique=False)
    camExpireDate = db.Column('cam_expire_date', db.DateTime, nullable=True, unique=False)
    createdDate = db.Column('createdDate', db.DateTime, nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime, nullable=True,  unique=False, onupdate=func.now())
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    # supplies = db.relationship('Post', backref='driver', lazy='dynamic')

    def __repr__(self):
        return '<Driver {}>'.format(self.name)   

# Product Schema
class DriverSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'birthDate', 'ccNumber', 'ccExpireDate', 'driverLicenseNumber', 'driverLicenseExpireDate', 'tccExpireDate', 'camExpireDate', 'userid')

# Init schema
driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)


# class Supply(db.Model):
 
#     __tablename__ = 'supplies'

#     id = db.Column('supply_id', db.Integer, primary_key=True)
    
#     created_date = db.Column('created_date', db.DateTime, nullable=False,  unique=False, server_default=func.now())
#     modified_date = db.Column('modified_date', db.DateTime, nullable=True,  unique=False, onupdate=func.now())
#     driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    