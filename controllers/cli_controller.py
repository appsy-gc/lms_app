# Blueprint
from flask import Blueprint
from init import db
from models.student import Student

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables create")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables YEET'd")

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

    db.session.add_all(students)

    db.session.commit()

    print("Tables impregnated")