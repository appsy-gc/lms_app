# Import packages
import os
from flask import Flask
# Import from init.py
from init import db, ma

def create_app():
    # Initialise
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    return app