import numpy as np
import cv2
import os
from database_models import *



class DbOperations:
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))

    def get_user_by_username(self,username):
        return User.query.filter(User.username == username).first()

    def get_employee_name(self,id):
        employee =  Employee.query.get(id)
        name = 'Unknown';
        if employee:
            name = f'{employee.lastname} {employee.firstname}'
        return name


    # get employee by name
    def get_employee(self, name):
        try:
            return Employee.query.filter(Employee.firstname == name).first()
        except Exception as error:
            print("ERROR DB: ", error)
            return {}
        finally:
            return {}

    # save new employee
    def save_employee(self, employee):
        try:
            db.session.add(employee)
            saved = db.session.commit()
            return employee
        except Exception as error:
            print("ERROR DB: ", error)
            return False
        finally:
            return False

    # save new attendance record
    def save_attendance(self, data):
        try:
            found = Attendance.query.filter(Attendance.employee_id == data['id']).filter(
                Attendance.date == data['date']).first()

            # get today's record for user
            if found:
                image_path = f"{self.FILE_PATH}/static/img/attendance/{data['date']}/{data['id']}/departure.jpg"
                os.makedirs(f"{self.FILE_PATH}/static/img/attendance/{data['date']}/{data['id']}", exist_ok=True)
                cv2.imwrite(image_path, np.array(data['picture_data']))
                data['picture_path'] =  f"{data['date']}/{data['id']}/departure.jpg"
                # if found, update time out,
                found.departure_time = data['hour']
                found.departure_picture = data['picture_path']

                db.session.add(found)
                db.session.commit()
            else:
                # else create time in record
                image_path = f"{self.FILE_PATH}/static/img/attendance/{data['date']}/{data['id']}/arrival.jpg"
                os.makedirs(f"{self.FILE_PATH}/static/img/attendance/{data['date']}/{data['id']}", exist_ok=True)
                cv2.imwrite(image_path, np.array(data['picture_data']))
                data['picture_path'] = f"{data['date']}/{data['id']}/arrival.jpg"

                attend = Attendance()
                attend.employee_id  = data['id']
                attend.arrival_time = data['hour']
                attend.date = data['date']
                attend.arrival_picture = data['picture_path']
                db.session.add(attend)
                db.session.commit()

        except Exception as error:
            print("ERROR DB: ", error)
        finally:
            result = {}
        return result

    def save_department(self, name):
        try:
            return True
            #depart = Department()
        except Exception as error:
            print("ERROR DB: ", error)
        finally:
            result = {}
        return result
