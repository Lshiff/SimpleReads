from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
POSTGRES_URI = os.getenv('POSTGRES_URI')
if not POSTGRES_URI:
    print("NO ADDRESS")
    exit()

app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
app.config["SECRET_KEY"] = "dAah3fxjuDA6v7O1C6nIAj2vdgrp5BqE"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

from finalproject import routes
