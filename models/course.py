from init import db, ma
from marshmallow import fields

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    duration = db.Column(db.Float, nullable=False)
    # Set up foreign key from the teachers table (not the model)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    # Must refer to the teachers model, not table
    teacher = db.relationship("Teacher", back_populates="courses") # One teacher can have multiple courses
    # cascade to delete enrolments if a course is deleted
    enrolments = db.relationship("Enrolment", back_populates="course", cascade="all, delete")

class CourseSchema(ma.Schema):
    # Order data in output as shown below, rather than alphabetically which is default
    ordered=True
    # Tell marshmallow how to seralise the data from teacher table
    teacher = fields.Nested("TeacherSchema", only=["name", "department"])
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=["course"]))
    class Meta:
        fields = ("id", "name", "duration", "teacher_id", "teacher", "enrolments")

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

