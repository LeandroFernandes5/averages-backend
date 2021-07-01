from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow 
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# 
#   Get environment configuration 
#  
app.config.from_object(Config)

#
#    Adding Db object and Migration Engine
#
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

# 
#    Import views
#
from app.views import users, drivers, gasstations, cars, supplies
from app import models
from app.serialization import UserSchema, DriverSchema


