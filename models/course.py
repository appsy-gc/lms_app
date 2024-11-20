from init import db, ma

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    duration = db.Column(db.Float, nullable=False)
    # Set up foreign key from the teachers table (not the model)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

class CourseSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "duration", "teacher_id")

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

