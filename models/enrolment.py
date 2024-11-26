from init import db, ma
from marshmallow import fields

class Enrolment(db.Model):
    __tablename__ = "enrolments"
    # Create constraint
    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", name="unique_student_course"),
    )

    id = db.Column(db.Integer, primary_key=True)
    enrolment_date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    # Create relationships 
    student = db.relationship("Student", back_populates="enrolments")
    course = db.relationship("Course", back_populates="enrolments")

class EnrolmentSchema(ma.Schema):
    ordered=True
    # Tell marshmallow how to serialise
    student = fields.Nested("StudentSchema", only=["name", "email"])
    course = fields.Nested("CourseSchema", only=["name", "duration"])
    class Meta:
        fields = ("id", "enrolment_date", "student_id", "teacher_id", "student", "course")

enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many=True)