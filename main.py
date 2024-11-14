# Import packages
from flask import Flask
# Import from init.py
from init import db, ma

def create_app():
    # Initialise
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://lms_dev:123456@localhost:5432/lms_app_db"

    db.init_app(app)
    ma.init_app(app)

    return app