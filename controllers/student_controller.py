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
      body_data = request.get_json()
      new_student = Student(
           name = body_data.get("name"),
           email = body_data.get("email"),
           address = body_data.get("address")
      )
      db.session.add(new_student)
      db.session.commit()
      return StudentSchema().dump(new_student), 201
      
# @app.route("/products", methods=["POST"])
# def create_product():
#     # Import request from flask
#     body_data = request.get_json()
#     # New instance of Product class and use keys from body_data to assign values
#     new_product = Product(
#         name = body_data.get("name"),
#         description = body_data.get("description"),
#         price = body_data.get("price"),
#         stock = body_data.get("stock")
#     )
#     db.session.add(new_product)
#     db.session.commit()
#     return product_schema.dump(new_product), 201 # 201 Created code returned

# Update - /students/id - PUT or PATCH


# Delete - /students/id - DELETE

