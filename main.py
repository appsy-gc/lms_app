# Import packages
import os
from flask import Flask
from marshmallow.exceptions import ValidationError

# Import from init.py
from init import db, ma

# Import blueprint from cli_controller
from controllers.cli_controller import Blueprint, db_commands
# Import blueprint from student_controller
from controllers.student_controller import students_bp
# Import blueprint from teacher_controller
from controllers.teacher_controller import teachers_bp
# Import blueprint from course_controller
from controllers.course_controller import courses_bp
# Import blueprint from enrolments_controler
from controllers.enrolment_controller import enrolments_bp

def create_app():
    # Initialise
    app = Flask(__name__)

    print("Server Started...")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Stop flask from ordering data
    app.json.sort_keys = False

    # Initialise SQLAlcemy
    db.init_app(app)
    # Initilise Marshmallow
    ma.init_app(app)

    # Glogal error handling by marshmallow
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"message": err.messages}, 400

    # Register cli_controller 
    app.register_blueprint(db_commands)
    # Register student_controller 
    app.register_blueprint(students_bp)
    # Register teacher_controller
    app.register_blueprint(teachers_bp)
    # Register course_controller
    app.register_blueprint(courses_bp)
    # Register enrolment_controller
    app.register_blueprint(enrolments_bp)

    return app