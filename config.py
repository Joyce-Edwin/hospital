from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


import os

app = Flask(__name__)

BASE_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Mdelisa2@localhost/hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'this is secret'

# init DB(object creation)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
