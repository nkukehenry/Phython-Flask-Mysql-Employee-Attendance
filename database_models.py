from sqlalchemy import Table, Column, Integer, ForeignKey
from starter import db
from flask_login import UserMixin


# * ---------- DATABASE TABLE MODELS --------- *

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(300))
    employee_id = db.Column(db.Integer(), nullable=True)
    photo = db.Column(db.String(100), nullable=True)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    department = db.Column(db.String(50), nullable=True)
    staffid = db.Column(db.String(30), nullable=True)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, ForeignKey(Employee.id))
    arrival_time = db.Column(db.String(50), nullable=True)
    arrival_picture = db.Column(db.String(255), nullable=True)
    departure_time = db.Column(db.String(50), nullable=True)
    departure_picture = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(25), nullable=True)


class Timelog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    date = db.Column(db.String(50))
    arrival_time = db.Column(db.String(50))
    departure_time = db.Column(db.String(50))
    hours = db.Column(db.String(50))
    time_worked = db.Column(db.String(25))


class Timetotals(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.String(50))
        hours = db.Column(db.String(50))

# employee = db.relationship(Employee, backref= Employee.id, primaryjoin= employee_id == Employee.id, lazy='joined')
