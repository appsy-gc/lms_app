from flask import Blueprint, request
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
      # Get information from request body
      body_data = request.get_json()
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

# Update - /students/id - PUT or PATCH
@students_bp.route("/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
     stmt = db.select(Student).filter_by(id=student_id)
     student = db.session.scalar(stmt)
     body_data = request.get_json()

     if student:
          # Update with new data or use existing if new data not provided
          student.name = body_data.get("name") or student.name
          student.email = body_data.get("email") or student.email
          student.address = body_data.get("address") or student.address
          db.session.commit()
          return StudentSchema().dump(student)
     else:
          # Error message if student doesn't exist
          return {"message": f"Student with id: {student_id} does not exist"}, 404

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