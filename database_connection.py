import mysql.connector

class Connector:

    def __init__(self):
        self.connection_info = mysql.connector.connect(user = 'root',
                                         password= 'c!rist!ana25@',
                                         host= 'localhost',
                                         database= 'university_attendance',
                                         port= '3306')
        self.mycursor = self.connection_info.cursor()


