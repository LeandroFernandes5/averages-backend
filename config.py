import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = 'postgresql:///averages:averages@localhost:6543/flask' ##os.environ.get('DATABASE_URL') or print('No DB URI')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://averages:averages@localhost:6543/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_TIME_MIN = 60


class ProductionConfig(Config):
    PRODUCTION = True
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

