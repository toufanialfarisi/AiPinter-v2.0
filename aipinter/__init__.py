import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow

UPLOAD_FOLDER = os.getcwd() + '/aipinter/static/image_vision'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# initiate FLASK APP 
app = Flask(__name__)

# initiate databse using SQL ALCHEMY
db = SQLAlchemy(app)

# initiate flask marshamllow object
ma = Marshmallow(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# create database file using sqlite
file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + basedir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a secret key
app.config['SECRET_KEY'] = 'aipinter291195'

# Initiate flask migration for updating the database in app
Migrate(app, db)


# create login utility
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

# BLUEPRINT REGISTRATION
from aipinter.core.views import core
from aipinter.users.views import users
from aipinter.error_pages.handlers import error_pages
from aipinter.vision.views import vision
from aipinter.camera.views import cam
from aipinter.blogpost.views import blogpost
from aipinter.ocr.views import ocreg

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(vision)
app.register_blueprint(cam)
app.register_blueprint(blogpost)
app.register_blueprint(ocreg)