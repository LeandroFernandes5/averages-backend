from flask import Flask, make_response
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
#   Import utils
#
from app.util import *

# 
#    Import Routes
#
from app.models import *
from app.carAverages.routes import *
from app.cars.routes import *
from app.drivers.routes import *
from app.gasStations.routes import *
from app.supplies.routes import *
from app.users.routes import *
from app.me.routes import *

# 
#    Import Schema
#
from app.carAverages.schema import *
from app.cars.schema import *
from app.drivers.schema import *
from app.gasStations.schema import *
from app.supplies.schema import *
from app.users.schema import *




