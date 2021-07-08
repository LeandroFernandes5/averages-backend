import os
from random import *
import csv
from sqlalchemy import Column, Integer, String,  create_engine, insert, MetaData, Table, DateTime, Float, Boolean
from werkzeug.security import generate_password_hash
import datetime


dbURI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://averages:averages@localhost:6543/flask'     

engine = create_engine(dbURI, echo = True)

conn = engine.connect()
meta = MetaData()

tables = engine.table_names()
print(tables)
for table in tables:
    if table == 'alembic_version':
        pass
    else:
        conn.engine.execute('TRUNCATE TABLE ' + table + ' RESTART IDENTITY CASCADE')


##
#   Insert Users
##

users = Table('users', 
meta,
Column('email', String(128), index=True, unique=True, nullable=False),
Column('password', String(128), nullable=False, unique=False),
Column('name', String(64), nullable=True, unique=False),
Column('role', String(64), nullable=False, unique=False, server_default='User'),
Column('status', String(64), nullable=False, unique=False, server_default='Pending'),
)

with open('users.csv') as csvfile:
     userader = csv.reader(csvfile, delimiter=',')
     for row in userader:
        conn.engine.execute(insert(users).
            values(
                email= row[0], 
                name= row[1], 
                password=generate_password_hash(row[2]),
                role=row[3],
                status=row[4]
                )
        )


##
#   Insert Gas Stations
##

gas = Table('gasstations', 
meta,
Column('name', String(128), index=True, unique=True, nullable=False)
)

with open('gasStations.csv') as csvfile:
     userader = csv.reader(csvfile, delimiter=',')
     for row in userader:
        conn.engine.execute(insert(gas).
            values(
                name= row[0]
                )
        )


 
##
#   Insert Drivers
##

drivers = Table('drivers', 
meta,
Column('name', String(64), nullable=False, unique=False),
Column('birthDate', DateTime(timezone=True), nullable=True, unique=False),
Column('ccNumber', String(64), nullable=True, unique=False),
Column('ccExpireDate', DateTime(timezone=True), nullable=True, unique=False),
Column('driverLicenseNumber', String(64), nullable=True, unique=False),
Column('driverLicenseExpireDate', DateTime(timezone=True), nullable=True, unique=False),
Column('tccExpireDate', DateTime(timezone=True), nullable=True, unique=False),
Column('camExpireDate', DateTime(timezone=True), nullable=True, unique=False),
Column('userId', Integer)
)

with open('drivers.csv') as csvfile:
     userader = csv.reader(csvfile, delimiter=',')
     for row in userader:
        try:
             conn.engine.execute(insert(drivers).
                values(
                    name = row[0],
                    birthDate = datetime.datetime.now() - datetime.timedelta(weeks=randint(2000, 3000)),
                    ccNumber = row[1],
                    ccExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(40, 80)),
                    driverLicenseNumber = row[2],
                    driverLicenseExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(10, 40)),
                    tccExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(5, 12)),
                    camExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(15, 23)),
                    userId = row[3]
                    ))
        except IndexError:
            conn.engine.execute(insert(drivers).
                values(
                    name = row[0],
                    birthDate = datetime.datetime.now() - datetime.timedelta(weeks=randint(2000, 3000)),
                    ccNumber = row[1],
                    ccExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(40, 80)),
                    driverLicenseNumber = row[2],
                    driverLicenseExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(10, 40)),
                    tccExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(5, 12)),
                    camExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(15, 23))
                    )

        )

##
#   Insert Cars
##

cars = Table('cars', 
meta,
Column('plate', String(64), nullable=False, unique=False),
Column('brand', String(64), nullable=True, unique=False),
Column('model', String(64), nullable=True, unique=False),
Column('registerDate', DateTime(timezone=True), nullable=True, unique=False),
Column('chassisNo', String(64), nullable=True, unique=False),
Column('obraNo', String(64), nullable=True, unique=False),
Column('inspectionDate', DateTime(timezone=True), nullable=True, unique=False),
Column('tccExpireDate', DateTime(timezone=True), nullable=True, unique=False),
Column('licenseExpireDate', DateTime(timezone=True), nullable=True, unique=False),
Column('tachographDate', DateTime(timezone=True), nullable=True, unique=False),
Column('status', String(64), nullable=False, unique=False, server_default='Active')
)

with open('cars.csv') as csvfile:
     userader = csv.reader(csvfile, delimiter=',')
     for row in userader:
            conn.engine.execute(insert(cars).
            values(
                plate= row[0],
                brand=row[1],
                model=row[2],
                registerDate=datetime.datetime.now() - datetime.timedelta(weeks=randint(400, 1000)),
                chassisNo=row[3],
                obraNo=row[4],
                inspectionDate= datetime.datetime.now() + datetime.timedelta(weeks=randint(10, 40)),
                tccExpireDate= datetime.datetime.now() + datetime.timedelta(weeks=randint(400, 1000)),
                licenseExpireDate = datetime.datetime.now() + datetime.timedelta(weeks=randint(20, 50)),
                tachographDate=datetime.datetime.now() + datetime.timedelta(weeks=randint(400, 1000)),
                status=row[5]
                ))


##
#   Insert Supplies
##

supplies = Table('supplies', 
meta,
Column('totalKm', Integer, nullable=False, unique=False),
Column('liters', Float(precision=10, decimal_return_scale=2), nullable=False, unique=False),
Column('fullTank', Boolean, nullable=False, unique=False),
Column('cost', Float(precision=10, decimal_return_scale=2), nullable=False, unique=False, default=0),
Column('supplyDate', DateTime(timezone=True), nullable=False,  unique=False),
Column('average', Float(precision=10, decimal_return_scale=2), nullable=False, unique=False),
Column('driverId', Integer),
Column('gasStationId',Integer),
Column('carId',Integer),
)

with open('supplies.csv') as csvfile:
     userader = csv.reader(csvfile, delimiter=',')
     for row in userader:
            conn.engine.execute(insert(supplies).
            values(
                totalKm = randint(50,10000),
                liters = randint(10,30),
                fullTank = random() < 0.5,
                supplyDate = datetime.datetime.now() - datetime.timedelta(weeks=randint(1, 3)),
                average = row[0],
                driverId = randint(1, 2),
                gasStationId = randint(1, 3),
                carId = randint(1, 3)
                ))