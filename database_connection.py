import mysql.connector

class Connector:

    def __init__(self):
        self.connection_info = mysql.connector.connect(user = 'root',
                                         password= 'A12345%z',
                                         host= 'localhost',
                                         database= 'university_attendece',
                                         port= '3306')
        self.mycursor = self.connection_info.cursor()


