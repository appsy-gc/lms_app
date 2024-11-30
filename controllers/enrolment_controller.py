from flask import Blueprint, request
from init import db
from  models.enrolment import Enrolment, EnrolmentSchema
# Import specific exception type from SQLAlcemy
from sqlalchemy.exc import IntegrityError
# Import error codes so we don't have to remember them
from psycopg2 import errorcodes

enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/enrolments")


# GET all enrolments (/enrolments)
@enrolments_bp.route("/")
def get_enrolments():
    student_id = request.args.get("student_id")

    if student_id:
         stmt = db.select(Enrolment).filter_by(student_id=student_id)
    else:
        stmt = db.select(Enrolment).order_by(Enrolment.id)

    enrolment_list = db.session.scalars(stmt)
    return EnrolmentSchema(many=True).dump(enrolment_list)


# GET an enrolment (/enrolments/course_id)
@enrolments_bp.route("/<int:enrolment_id>")
def get_enrolment(enrolment_id):
    stmt = db.select(Enrolment).filter_by(id=enrolment_id)
    enrolment = db.session.scalar(stmt)

    if enrolment:
        return EnrolmentSchema().dump(enrolment)
    else:
        return {"message": f"Enrolment with id '{enrolment_id}' does not exist"}, 404


# POST an enrolment (/enrolments)
@enrolments_bp.route("/", methods=["POST"])
def create_enrolment():
    try:
        body_data = request.get_json()

        new_enrolment = Enrolment(
            enrolment_date = body_data.get("enrolment_date"),
            student_id = body_data.get("student_id"),
            course_id = body_data.get("course")
        )
        db.session.add(new_enrolment)
        db.session.commit()
        return EnrolmentSchema().dump(new_enrolment), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violoation
            # Return specific field that is in violoation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique_constraint_violoation
            return {"message": err.orig.diag.message_detail}, 409


# PUT or PATCH an enrolment (/enrolments/enrolment_id)
@enrolments_bp.route("/<int:enrolment_id>", methods=["PUT", "PATCH"])
def update_enrolment(enrolment_id):
     stmt = db.select(Enrolment).filter_by(id=enrolment_id)
     enrolment = db.session.scalar(stmt)
     body_data = request.get_json()

     if enrolment:
          enrolment.enrolment_date = body_data.get("enrolment_date") or enrolment.enrolment_date
          enrolment.student_id = body_data.get("student_id") or enrolment.student_id
          enrolment.course = body_data.get("course") or enrolment.course
          db.session.commit()
          return EnrolmentSchema().dump(enrolment)
     else:
          {"message": f"Enrolment with id '{enrolment.id}' does not exist"}, 404
          


# DELETE an enrolment (/enrolments)
@enrolments_bp.route("/<int:enrolment_id>", methods=["DELETE"])
def delete_enrolment(enrolment_id):
     stmt = db.select(Enrolment).filter_by(id=enrolment_id)
     enrolment = db.session.scalar(stmt)

     if enrolment:
          db.session.delete(enrolment)
          db.session.commit()
          return {"message": f"enrolment: '{enrolment.id}' deleted successfully"}
     else:
          return {"message": f"Enrolment with id: '{enrolment_id}' does not exist"}, 404