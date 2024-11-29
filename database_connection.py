import mysql.connector

class Connector:

    def __init__(self):
        self.connection_info = mysql.connector.connect(user = 'root',
                                         password= 'A12345%z',
                                         host= 'localhost',
                                         database= 'university_attendance',
                                         port= '3306')
        self.mycursor = self.connection_info.cursor()

    def get_faces_from_db(self):
        if self.mycursor is None:
            print("Database connection failed. Exiting...")
            return
        cursor = self.mycursor
        query = "select student_id, student_picture from student_images where student_id  in (15, 6, 1);"
        self.mycursor.execute(query)
        data = cursor.fetchall()
        return data

    def get_course_group(self):
        if self.mycursor is None:
            print("Database connection failed. Exiting...")
            return
        cursor = self.mycursor
        query = "select * from course_group_name;"
        self.mycursor.execute(query)
        data = cursor.fetchall()
        return data

