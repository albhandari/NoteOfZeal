from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from flask_login import LoginManager


myobj = Flask(__name__)

myobj.config.from_mapping(
    SECRET_KEY = 'somesecretkey',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'web.db'),

)

db = SQLAlchemy(myobj)
logging = LoginManager(myobj)
logging.init_app(myobj)
logging.login_view = 'login' 

from website import routes, models

