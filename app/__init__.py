from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from .models import *

app = Flask(__name__)

# 
#   Get environment configuration 
#  
app.config.from_object(Config)

#
#    Adding Db object and Migration Engine
#
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 
#    Import views
#
from app.views import auth
from app import models


