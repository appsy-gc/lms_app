from flask import Blueprint, request
from init import db
from models.student import Student, StudentSchema
# Import specific exception type from SQLAlcemy
from sqlalchemy.exc import IntegrityError
# Import error codes so we don't have to remember them
from psycopg2 import errorcodes

students_bp = Blueprint("students", __name__, url_prefix="/students")

# Read all - /students - GET
@students_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt)
    data = StudentSchema(many=True).dump(students_list)

    return data

# Read one - /students/id - GET
@students_bp.route("/<int:student_id>")
def get_student(student_id):
        stmt = db.select(Student).filter_by(id=student_id)
        student = db.session.scalar(stmt)

        if student:
            data = StudentSchema().dump(student)
            return data
        else:
            return {"message": f"Student with id: {student_id} does not exist, soz chump"}, 404

# Create - /students - POST
@students_bp.route("/", methods=["POST"])
def create_student():
      # Try Except block to handle error when the same student is added
      try:
        # Get information from request body
        body_data = StudentSchema().load(request.get_json(), partial=True)
        # Create student instance
        new_student = Student(
            name = body_data.get("name"),
            email = body_data.get("email"),
            address = body_data.get("address")
        )
        # Add new student data
        db.session.add(new_student)
        # Commit changes
        db.session.commit()
        return StudentSchema().dump(new_student), 201
      except IntegrityError as err:
           print(err.orig.pgcode)
           if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                # not_null_violoation
                # Return specific field that is in violoation
                return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
           if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                 # unique_constraint_violoation
                 return {"message": "Data already exists. Update student details instead"}, 409


# Update - /students/id - PUT or PATCH
@students_bp.route("/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
     try:
        # Find the student with specific ID
        stmt = db.select(Student).filter_by(id=student_id)
        student = db.session.scalar(stmt)
        # Get the data to be updated
        body_data = StudentSchema().load(request.get_json(), partial=True)

        if student:
            # Update with new data or use existing if new data not provided
            student.name = body_data.get("name") or student.name
            student.email = body_data.get("email") or student.email
            student.address = body_data.get("address") or student.address
            # Commit
            db.session.commit()
            # Return updated data
            return StudentSchema().dump(student)
        else:
            # Error message if student doesn't exist
            return {"message": f"Student with id: {student_id} does not exist"}, 404
     except IntegrityError as err:
          print(err.orig.pgcode)
          if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                 # unique_constraint_violoation
                 return {"message": "Email already exists."}, 409


# Delete - /students/id - DELETE
@students_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
     stmt = db.select(Student).filter_by(id=student_id)
     student = db.session.scalar(stmt)

     if student:
          db.session.delete(student)
          db.session.commit()
          return {"message": f"Student: '{student.name}' deleted successfully"}
     else:
          return {"message": f"Student with id: '{student_id}' does not exist"}, 404