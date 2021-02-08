"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
# to get rid of the follwoing warrning
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning
SQLALCHEMY_TRACK_MODIFICATIONS = False 

UPLOAD_LOCATION = "D:\\web development\\semester6project\\static\\uploadedimg"