from flask import Blueprint, request
from init import db
from models.course import Course, CourseSchema
# Import specific exception type from SQLAlcemy
from sqlalchemy.exc import IntegrityError
# Import error codes so we don't have to remember them
from psycopg2 import errorcodes

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

# Read all - /courses - GET
@courses_bp.route("/")
def get_courses():
    stmt = db.select(Course).order_by(Course.id)
    courses_list = db.session.scalars(stmt)
    data = CourseSchema(many=True).dump(courses_list)
    return data


# Read one - /courses/id - GET
@courses_bp.route("/<int:course_id>")
def get_course(course_id):
        stmt = db.select(Course).filter_by(id=course_id)
        course = db.session.scalar(stmt)

        if course:
            return CourseSchema().dump(course)
        else:
            return {"message": f"Course with id: {course_id} does not exist, soz chump"}, 404

# Create - /courses - POST
@courses_bp.route("/", methods=["POST"])
def create_course():
      # Try Except block to handle error when the same course is added
      try:
        # Get information from request body
        body_data = request.get_json()
        # Create course instance
        new_course = Course(
            name = body_data.get("name"),
            duration = body_data.get("duration"),
            teacher_id = body_data.get("teacher_id")
        )
        # Add new course data
        db.session.add(new_course)
        # Commit changes
        db.session.commit()
        return CourseSchema().dump(new_course), 201
      except IntegrityError as err:
           print(err.orig.pgcode)
           if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                # not_null_violoation
                # Return specific field that is in violoation
                return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
           if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                 # unique_constraint_violoation
                 return {"message": "Data already exists. Update course details instead"}, 409


# Update - /teachers/id - PUT or PATCH
@courses_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    # Find the student with specific ID
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    # Get the data to be updated
    body_data = request.get_json()

    if teacher:
        # Update with new data or use existing if new data not provided
        teacher.name = body_data.get("name") or teacher.name
        teacher.department = body_data.get("department") or teacher.department
        teacher.address = body_data.get("address") or teacher.address
        # Commit
        db.session.commit()
        # Return updated data
        return CourseSchema().dump(teacher)
    else:
        # Error message if student doesn't exist
        return {"message": f"Teacher with id: {teacher_id} does not exist"}, 404


# Delete - /teachers/id - DELETE
@courses_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
     stmt = db.select(Teacher).filter_by(id=teacher_id)
     teacher = db.session.scalar(stmt)

     if teacher:
          db.session.delete(teacher)
          db.session.commit()
          return {"message": f"teacher: '{teacher.name}' deleted successfully"}
     else:
          return {"message": f"Teacher with id: '{teacher_id}' does not exist"}, 404