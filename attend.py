from db_ops import DbOperations
import time

dbOps = DbOperations()
class Attend:

    def capture(self,id,picture):
        print(f'ID: {id}')
        attendance = {}
        attendance['id'] = id
        attendance['hour'] = f'{str(time.localtime().tm_hour)}:{str(time.localtime().tm_min)}'
        attendance[
            'date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
        attendance['picture_data'] = picture
        # SEND TO DB
        dbOps.save_attendance(attendance)
        return dbOps.get_employee_name(id)