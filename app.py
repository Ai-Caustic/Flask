from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData
import os

meta = MetaData()


# Init app
app = Flask(__name__)
# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Course Model
class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(100), unique=True)
    faculty = db.Column(db.String(50))
    course_desc = db.Column(db.String(256))
    qualification = db.Column(db.String(2))

    def __init__(self, course_id, course_name, faculty, course_desc, qualify):
        self.course_id = course_id
        self.course_name = course_name
        self.faculty = faculty
        self.course_desc = course_desc
        self.qualify = qualify


# Course schema
class CourseSchema(ma.Schema):
    class Meta:
        fields = ("course_id", "course_name", "faculty", "course_desc", "qualify")


# Student Model
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_name = db.Column(db.String(256))
    is_qualified = db.Column(db.Boolean)
    email = db.Column(db.String(256), unique=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"))

    def __init__(self, student_id, student_name, is_qualified, email, course_id):
        self.student_id = student_id
        self.student_name = student_name
        self.is_qualified = is_qualified
        self.email = email
        self.course_id = course_id


# Student schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ("student_id", "student_name", "is_qualified", "email", "course_id")


# Unit Model
class Unit(db.Model):
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(150), unique=True)
    category = db.Column(db.String)
    credit_hrs = db.Column(db.Float)
    description = db.Column(db.String(256))

    def __init__(self, unit_id, unit_name, category, credit_hrs, description):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.category = category
        self.credit_hrs = credit_hrs
        self.description = description


# Unit schema
class UnitSchema(ma.Schema):
    class Meta:
        fields = ("unit_id", "unit_name", "category", "credit_hrs", "description")


# Join Table for Units & Courses
class UnitCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"))
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.unit_id"))
    semester = db.Column(db.string(20))
    year__ = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))

    def __init__(self, id, course_id, unit_id, semester, year__, student_id):
        self.id = id
        self.unit_id = unit_id
        self.course_id = course_id
        self.semester = semester
        self.year__ = year__
        self.student_id = student_id


# UnitCourse Schema
class UnitCourseSchema:
    class Meta:
        fields = ("id", "course_id", "unit_id", "semester", "year__", "student_id")


# Init schema
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
unit_schema = UnitSchema()
unit_schema = UnitSchema(many=True)
unitcourse_schema = UnitCourseSchema()
unitcourses_schema = UnitCourseSchema(many=True)


# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
