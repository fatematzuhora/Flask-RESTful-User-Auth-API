from os import environ, path

BASE_DIR = path.abspath(path.dirname(__file__))



# config class
class Config(object):
    """set Flask configuration variables from .env file."""

    # general
    DEBUG = environ.get('DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + path.join(BASE_DIR, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    # security
    SALT_KEY = environ.get('SALT_KEY')