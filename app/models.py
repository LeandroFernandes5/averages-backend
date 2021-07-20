from sqlalchemy.orm import backref, relationship
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

#
#   Database representation for ORM use
#
class User(db.Model):
 
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(128), index=True, unique=True, nullable=False)
    password = db.Column('password', db.String(128), nullable=False, unique=False)
    name = db.Column('name', db.String(64), nullable=True, unique=False)
    role = db.Column('role', db.String(64), nullable=False, unique=False, server_default='User')
    passwordResetToken = db.Column('passwordResetToken', db.String(128), nullable=True,  unique=False)
    imageURL = db.Column('imageURL', db.String(128), nullable=True, unique=False)
    status = db.Column('status', db.String(64), nullable=False, unique=False, server_default='Pending')
    createdDate = db.Column('createdDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime(timezone=True), nullable=True,  unique=False, onupdate=func.now())
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
    imageURL = db.Column('imageURL', db.String(128), nullable=True, unique=False)
    name = db.Column('name', db.String(64), nullable=False, unique=False)
    birthDate = db.Column('birthDate', db.DateTime(timezone=True), nullable=True, unique=False)
    ccNumber = db.Column('ccNumber', db.String(64), nullable=True, unique=False)
    ccExpireDate = db.Column('ccExpireDate', db.DateTime(timezone=True), nullable=True, unique=False)
    driverLicenseNumber = db.Column('driverLicenseNumber', db.String(64), nullable=True, unique=False)
    driverLicenseExpireDate = db.Column('driverLicenseExpireDate', db.DateTime(timezone=True), nullable=True, unique=False)
    tccExpireDate = db.Column('tccExpireDate', db.DateTime(timezone=True), nullable=True, unique=False)
    camExpireDate = db.Column('camExpireDate', db.DateTime(timezone=True), nullable=True, unique=False)
    createdDate = db.Column('createdDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime(timezone=True), nullable=True,  unique=False, onupdate=func.now())
    userId = db.Column('userId', db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Driver {}>'.format(self.name)   


class Car(db.Model):

    __tablename__ = 'cars'

    id = db.Column('id', db.Integer, primary_key=True)
    plate = db.Column('plate', db.String(64), nullable=False, unique=False)
    brand = db.Column('brand', db.String(64), nullable=True, unique=False)
    model = db.Column('model', db.String(64), nullable=True, unique=False)
    registerDate = db.Column('registerDate', db.DateTime(timezone=True), nullable=True, unique=False)
    chassisNo = db.Column('chassisNo', db.String(64), nullable=True, unique=False)
    obraNo = db.Column('obraNo', db.String(64), nullable=True, unique=False)
    inspectionDate = db.Column('inspectionDate', db.DateTime(timezone=True), nullable=True, unique=False)
    tccExpireDate = db.Column('tccExpireDate', db.DateTime(timezone=True), nullable=True, unique=False)
    licenseExpireDate = db.Column('licenseExpireDate', db.DateTime(timezone=True), nullable=True, unique=False)
    tachographDate = db.Column('tachographDate', db.DateTime(timezone=True), nullable=True, unique=False)
    status = db.Column('status', db.String(64), nullable=False, unique=False, server_default='Active')
    createdDate = db.Column('createdDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime(timezone=True), nullable=True,  unique=False, onupdate=func.now())
    carAverage = relationship("CarAverage", uselist=False, backref="carAverages")

    def __repr__(self):
        return '<Car {}>'.format(self.plate)


class CarAverage(db.Model):

    __tablename__ = 'caraverages'

    id = db.Column('id', db.Integer, primary_key=True)
    liters = db.Column('liters', db.Float(precision=10, decimal_return_scale=2), nullable=False, unique=False)
    km = db.Column('km', db.Integer, nullable=False, unique=False)
    year = db.Column('year', db.Integer, nullable=False, unique=False)
    month = db.Column('month', db.Integer, nullable=False, unique=False)
    average = db.Column('average', db.Float(precision=10, decimal_return_scale=2), nullable=False, unique=False) 
    createdDate = db.Column('createdDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime(timezone=True), nullable=True,  unique=False, onupdate=func.now())
    carId = db.Column('carId', db.Integer, db.ForeignKey('cars.id'))

    def __repr__(self):
        return '<CarAverage {}>'.format(self.id)

class GasStation(db.Model):

    __tablename__ = 'gasstations'

    id = db.Column('id', db.Integer, primary_key=True)
    name = name = db.Column('name', db.String(64), nullable=False, unique=False)
    createdDate = db.Column('createdDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime(timezone=True), nullable=True,  unique=False, onupdate=func.now())

    def __repr__(self):
        return '<GasStation {}>'.format(self.name)


class Supply(db.Model):
 
    __tablename__ = 'supplies'

    id = db.Column('id', db.Integer, primary_key=True)
    totalKm = db.Column('totalKm', db.Integer, nullable=False, unique=False)
    liters = db.Column('liters', db.Float(precision=10, decimal_return_scale=2), nullable=False, unique=False)
    fullTank = db.Column('fullTank', db.Boolean, nullable=False, unique=False)
    cost =  db.Column('cost', db.Float(precision=10, decimal_return_scale=2), nullable=False, unique=False, default=0)
    supplyDate = db.Column('supplyDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    average = db.Column('average', db.Float(precision=10, decimal_return_scale=2), nullable=False, unique=False)
    createdDate = db.Column('createdDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime(timezone=True), nullable=True,  unique=False, onupdate=func.now())
    gasStationId = db.Column(db.Integer, db.ForeignKey('gasstations.id'))
    gasStation = relationship("GasStation")
    driverId = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    driver = relationship("Driver")
    carId = db.Column(db.Integer, db.ForeignKey('cars.id'))
    car = relationship("Car")
    
    def __repr__(self):
        return '<Supply {}>'.format(self.id)