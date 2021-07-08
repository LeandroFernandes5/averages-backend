import os
import csv
from sqlalchemy import Column, Integer, String,  create_engine, insert, MetaData, Table, DateTime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash


dbURI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://averages:averages@localhost:6543/flask'     

engine = create_engine(dbURI, echo = True)

conn = engine.connect()
meta = MetaData()

tables = engine.table_names()

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
                    name= row[0],
                    birthDate=row[1],
                    ccNumber=row[2],
                    ccExpireDate=row[3],
                    driverLicenseNumber=row[4],
                    driverLicenseExpireDate=row[5],
                    tccExpireDate=row[6],
                    camExpireDate=row[7],
                    userId = row[8]
                    ))
        except IndexError:
            conn.engine.execute(insert(drivers).
                values(
                    name= row[0],
                    birthDate=row[1],
                    ccNumber=row[2],
                    ccExpireDate=row[3],
                    driverLicenseNumber=row[4],
                    driverLicenseExpireDate=row[5],
                    tccExpireDate=row[6],
                    camExpireDate=row[7]
                    )

        )