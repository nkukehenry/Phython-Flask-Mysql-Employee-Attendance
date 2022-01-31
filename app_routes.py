import json
import os
from pprint import pprint
from datetime import datetime
import flask
import cv2
from flask import request, jsonify, Response, render_template, flash, url_for
from flask_cors import cross_origin
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from capture_images import EnrollCam
from data_schemas import TimelogSchema, TotalsSchema
from db_ops import DbOperations, db
from database_models import Employee, Attendance, Timelog, Timetotals
from auth_manager import *
from realtime_camera import LiveCam
from starter import app

dbOps = DbOperations()


# APP ENDPOINTS


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == 'GET':
        return render_template("sign_in.html")
    else:
        username = flask.request.form['username']
        password = flask.request.form['password']
        user = dbOps.get_user_by_username(username)
        right_pass = check_password_hash(user.password, password)
        #or not right_pass
        if not user :
            flash("Wrong user credentials")
            return render_template("sign_in.html")
        if user:
            login_user(user, remember=True)
            return flask.redirect(flask.url_for('attendance'))


@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))


@app.route('/live', methods=['GET'])
def feed():
    return render_template('feed.html')


@app.route('/attendance', methods=['GET'])
@login_required
def attendance():
    # attend_rows = Attendance.query.join(Employee).all()
    attend_rows = db.session.query(Attendance, Employee).filter(Attendance.employee_id == Employee.id).all()
    return render_template('attendance.html', records=attend_rows)


@app.route('/general', methods=['GET', 'POST'])
@login_required
def general():
    search = {'start': '', 'end': ''}
    if (request.method == 'GET'):
        attend_rows = db.session.query(Timelog).filter(Timelog.id == Employee.id).all()
    else:
        start_date = request.form['start']
        end_date = request.form['end']
        search = {'start': start_date, 'end': end_date}
        query = db.session.query(Timelog)
        if (start_date):
            query = query.filter(Timelog.date.between(start_date, end_date))
        attend_rows = query.all()
    return render_template('general_report.html', records=attend_rows, search=search)


@app.route('/individual_report', methods=['GET', 'POST'])
@login_required
def individual_report():
    search = {'start': '', 'end': '', 'employee': ''}
    employees = db.session.query(Employee).all()
    if (request.method == 'GET'):
        attend_rows = db.session.query(Timelog).filter(Timelog.id == 0).all()
    else:
        start_date = request.form['start']
        end_date = request.form['end']
        employee = request.form['employee']
        search = {'start': start_date, 'end': end_date, 'employee': employee}
        query = db.session.query(Timelog)
        if (start_date):
            query = query.filter(Timelog.date.between(start_date, end_date))
            query = query.filter(Timelog.employee_id == int(employee))
        attend_rows = query.all()
    return render_template('employee_report.html', employees=employees, records=attend_rows, search=search)


@app.route('/employee_graph', methods=['GET'])
def employee_graph():
    if (request.method == 'POST'):
        start_date = request.form['start']
        end_date = request.form['end']
        employee = request.form['employee']

        query = db.session.query(Timelog)
        if (start_date):
            query = query.filter(Timelog.date.between(start_date, end_date))
            query = query.filter(Timelog.employee_id == int(employee))
        attend_rows = query.all()
        empTotalsSchema = TimelogSchema(many=True)
        data = empTotalsSchema.dump(attend_rows)
        return jsonify(data)


@app.route('/general_graph', methods=['GET', 'POST'])
def general_graph():
    if (request.method == 'GET'):
        attend_rows = db.session.query(Timetotals).all()
    else:
        start_date = request.form['start']
        end_date = request.form['end']
        attend_rows = db.session.query(Timetotals).filter(Timetotals.date.between(start_date, end_date)).all()
    totalsSchema = TotalsSchema(many=True)
    data = totalsSchema.dump(attend_rows)
    return jsonify(data)


@app.route('/employees', methods=['GET'])
@login_required
def employees():
    employee_rows = Employee.query.all()
    return render_template('employees.html', employees=employee_rows)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'GET':
        employee_rows = Employee.query.all()
        return render_template('add_user.html', employees=employee_rows)
    else:
        try:
            existing = User.query.filter(User.employee_id == request.form['employee_id'])
            if not existing:
                user = User()
                user.username = request.form['username']
                user.employee_id = request.form['employee_id']
                user.password = generate_password_hash(request.form['password'])
                user.photo = ''
                db.session.add(user)
                db.session.commit()
                msg = 'User added successfully'
                flash(msg)
                return flask.redirect(flask.url_for('users'))
            else:
                flash('FAILED: Selected employee is already a system user')
                return flask.redirect(flask.url_for('add_user'))
        except:
            msg = 'FAILED:  Operation failed, try again'
            flash(msg)
            return flask.redirect(flask.url_for('add_user'))


@app.route('/users', methods=['GET'])
@login_required
def users():
    user_rows = db.session.query(User, Employee).filter(Employee.id == User.employee_id).all()
    return render_template('users.html', users=user_rows)


@app.route('/add_employee', methods=['GET'])
@login_required
def employee_form():
    return render_template('add_employee.html')


# fetch camera feed
@app.route('/enroll_feed/<string:id>', methods=['GET'])
def get_enroll_feed(id):
    return render_template('enroll_feed.html', id=id)


@app.route('/en_feed/<string:id>', methods=['GET'])
def get_employee_feed(id):
    camera = EnrollCam()
    feed = camera.get_feed(int(id))
    #  if type(feed) == type(True):
    # return Response( url_for('static',filename='feed.png'),mimetype='image/jpeg')
    return Response(feed, mimetype='multipart/x-mixed-replace; boundary=frame')


# fetch camera feed
@app.route('/feed', methods=['GET'])
def get_feed():
    camera = LiveCam()
    feed = camera.get_feed()
    return Response(feed, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test')
def test():
    camera = EnrollCam()
    feed = camera.get_feed(7)
    return Response(feed, mimetype='multipart/x-mixed-replace; boundary=frame')


# stop camera feed
@app.route('/stop', methods=['GET'])
def stop():
    cv2.VideoCapture(0).release()
    return 'Hello'


# get Employee by name
@app.route('/get_employee/<string:name>', methods=['GET'])
def search_employee(name):
    response = dbOps.get_employee(name);
    return jsonify(response)


# Add new employee to database
@app.route('/add_employee', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_employee():
    try:
        # Get the data & photo e from the request
        image_file = request.files['photo']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        department = request.form['department']
        staffid = request.form['staffid']

        employee = Employee()
        employee.firstname = firstname
        employee.lastname = lastname
        employee.department = department
        employee.staffid = staffid
        dbOps.save_employee(employee)

        pprint(vars(employee))

        # Save Photo for recognition
        file_path = os.path.join(f"static/img/users/{employee.id}.jpg")
        image_file.save(file_path)
        msg = 'Employee succesfully added'
        flash(msg)
        # return flask.redirect(flask.url_for('employees'))
        return flask.redirect(flask.url_for('get_enroll_feed', id=employee.id))
    except:
        msg = 'Error Occured, Please try again'
        flash(msg)  # employee_form
        return flask.redirect(flask.url_for('add_employee'))
