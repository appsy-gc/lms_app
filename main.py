# Import packages
import os
from flask import Flask

# Import from init.py
from init import db, ma

# Import blueprint from cli_controller
from controllers.cli_controller import Blueprint, db_commands
# Import blueprint from student_controller
from controllers.student_controller import students_bp
# Import blueprint from teacher_controller
from controllers.teacher_controller import teachers_bp
# Import blueprint from subject_controller

def create_app():
    # Initialise
    app = Flask(__name__)

    print("Server Started...")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Initialise SQLAlcemy
    db.init_app(app)
    # Initilise Marshmallow
    ma.init_app(app)

    # Register cli_controller 
    app.register_blueprint(db_commands)
    # Register student_controller 
    app.register_blueprint(students_bp)
    # Register teacher_controller
    app.register_blueprint(teachers_bp)

    # Register subject_controller

    return app