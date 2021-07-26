from sqlalchemy.orm import relationship
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func, extract

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

    def create_or_update_car_average(supDate, carId, result):
        
        avg = CarAverage.query.filter_by(year=supDate.year, month=supDate.month, carId = carId).first()
        
        if avg:

            avg.average = result['monthlyAvg']
            avg.liters = result['liters']
            avg.km = result['totalKm']

            app.logger.info('Updated Monthly Average with id: %s, liter: %s totalKm: %s, average: %s', avg.id, result['liters'], result['totalKm'], result['monthlyAvg'])

            return avg 

        else: 
            n = CarAverage(liters = result['liters'], km = result['totalKm'], year = supDate.year, month = supDate.month, carId = carId, average = result['monthlyAvg'])
            db.session.add(n)

            app.logger.info('Created Monthly Average with liter: %s totalKm: %s, average: %s', result['liters'], result['totalKm'], result['monthlyAvg'])

            return n

    def get_delete_car_average(supDate, carId):
        a = CarAverage.query.filter_by(year=supDate.year, month=supDate.month, carId = carId).first() 
        db.session.delete(a)
        return a

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
    isSupplyPast = db.Column('isSupplyPast', db.Boolean, nullable=False, unique=False, default=False)
    createdDate = db.Column('createdDate', db.DateTime(timezone=True), nullable=False,  unique=False, server_default=func.now())
    modifiedDate = db.Column('modifiedDate', db.DateTime(timezone=True), nullable=True,  unique=False, onupdate=func.now())
    gasStationId = db.Column(db.Integer, db.ForeignKey('gasstations.id'))
    gasStation = relationship("GasStation")
    driverId = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    driver = relationship("Driver")
    carId = db.Column(db.Integer, db.ForeignKey('cars.id'))
    car = relationship("Car")
    
    def get_next_sups(supDate, carId):
        return db.session.query(Supply).filter(Supply.supplyDate > supDate, Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.asc())

    def get_sup_range(supDate, carId):
        next = db.session.query(Supply).filter(Supply.supplyDate >= supDate , Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.asc())
        before = db.session.query(Supply).filter(Supply.supplyDate <= supDate, Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.desc())

        return db.session.query(Supply).filter(Supply.carId == carId, Supply.totalKm.between(before[1].totalKm, next[-1].totalKm)).order_by(Supply.totalKm.asc()) 

    def get_monthly_sup_range(supDate, carId):
        next = db.session.query(Supply).filter(extract('year', Supply.supplyDate) == supDate.year, extract('month', Supply.supplyDate) == supDate.month, Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.asc())

        return db.session.query(Supply).filter(Supply.carId == carId, Supply.totalKm.between(next[0].totalKm, next[-1].totalKm)).order_by(Supply.totalKm.asc()) 

    def get_aux_sups(supDate, carId):
        return db.session.query(Supply).filter(Supply.supplyDate >= supDate, Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.asc())

    def get_total_km(supDate, carId):
        max = db.session.query(db.func.max(Supply.totalKm)).filter(extract('year', Supply.supplyDate) == supDate.year, extract('month', Supply.supplyDate) == supDate.month, Supply.carId == carId, Supply.fullTank == True).scalar()
        min = db.session.query(db.func.min(Supply.totalKm)).filter(extract('year', Supply.supplyDate) == supDate.year, extract('month' , Supply.supplyDate) == supDate.month, Supply.carId == carId, Supply.fullTank == True).scalar()
        return max-min
        
    def get_liters_bt_sups(carId, aux):
        return db.session.query(func.sum(Supply.liters)).filter(Supply.carId == carId, Supply.totalKm.between(aux[1].totalKm, aux[-1].totalKm)).scalar() 

    def calc_average(liters, totalKm):
        return round((100 * liters) / totalKm, 2)

    def get_monthly_sups(supDate, carId):
        return db.session.query(Supply).filter(extract('year', Supply.supplyDate) == supDate.year, extract('month', Supply.supplyDate) == supDate.month, Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.asc())

    def __repr__(self):
        return '<Supply {}>'.format(self.id)