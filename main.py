# Import packages
import os
from flask import Flask

# Import from init.py
from init import db, ma

# Import blueprint from cli_controller
from controllers.cli_controller import Blueprint, db_commands
from controllers.student_controller import students_bp

def create_app():
    # Initialise
    app = Flask(__name__)

    print("Server Started...")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(students_bp)

    return app