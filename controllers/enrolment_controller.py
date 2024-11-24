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


# CREATE an enrolment (/enrolments)


# PUT or PATCH an enrolment (/enrolments/course_id)


# DELETE an enrolment (/enrolments)