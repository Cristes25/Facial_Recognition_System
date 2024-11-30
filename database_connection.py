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
        query = "select student_id, student_picture from student_images where student_id  in (15, 5, 1);"
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

    def get_schedule_id(self, data):
        query = """
SELECT distinct s.schedule_id, cs.class_group, c.course_code, c.course_name
from course_enrollment cs inner join courses c on c.course_code = cs.course_code
inner join schedules s on s.course_code = c.course_code
inner join days_of_week d ON s.day_id = d.day_id
WHERE  d.day_name = %s
  AND s.start_time <= %s
  AND s.end_time > %s;
        """

        # Execute the query
        self.mycursor.execute(query, data)
        result = self.mycursor.fetchall()
        return result
