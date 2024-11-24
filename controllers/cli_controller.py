# Blueprint
from flask import Blueprint
from init import db
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables create")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables YEET'd")

# Seed students table
@db_commands.cli.command("seed")
def seed_tables():
    students = [
        Student(
            name = "Appsy",
            email = "chris.e.apps@gmail.com",
            address = "A house"
        ),
        Student(
            name = "Student 2",
            email = "student2@gmail.com",
            address = "Another house"
        )
    ]

    teachers = [
        Teacher(
            name = "Mr Garrison",
            department = "Sociology",
            address = "Colorado"
        ),
        Teacher(
            name = "Mrs Krabappel",
            department = "English",
            address = "Springfield"
        )
    ]

    # If using foreign keys, ensure primary key is added and committed so it's available
    db.session.add_all(teachers)
    db.session.commit()

    courses = [
        Course(
            name = "Course 1",
            duration = 1,
            # Refers to the teachers created above
            teacher_id = teachers[0].id
        ),
        Course(
            name = "Course 2",
            duration = 2,
            teacher_id = teachers[0].id
        ),
        Course(
            name = "Course 3",
            duration = 1.5,
            teacher_id = teachers[1].id
        ),
        Course(
            name = "Course 4",
            duration = 3,
            teacher_id = teachers[1].id
        )
    ]

    enrolments = [
        Enrolment(
            enrolment_date = "2024-11-23",
            student = students[0],
            course = courses[0]
        ),
        Enrolment(
            enrolment_date = "2024-11-23",
            student = students[1],
            course = courses[0]
        ),
        Enrolment(
            enrolment_date = "2024-11-23",
            student = students[1],
            course = courses[1]
        )
    ]

    db.session.add_all(students)
    db.session.add_all(courses)
    db.session.add_all(enrolments)
    db.session.commit()
    print("Tables impregnated")