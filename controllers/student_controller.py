from flask import Blueprint
from init import db
from models.student import Student, StudentSchema

students_bp = Blueprint("students", __name__, url_prefix="/students")

# Read all - /students - GET
@students_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt)
    data = StudentSchema(many=True).dump(students_list)

    return data

# Read one - /students/id - GET


# Create - /students - POST


# Update - /students/id - PUT or PATCH


# Delete - /students/id - DELETE

