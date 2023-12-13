from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

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

from finalproject import routes
