import base64

import mysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from tensorflow.compiler.tf2xla.python.xla import select
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build
from database_connection import Connector

class  AttendanceReportGenerator:
    def __init__(self):
        self.connector = Connector()
        self.SCOPES=['https://www.googleapis.com/auth/gmail.send']
    def get_credentials(self):
        """
                Get Google API credentials directly from the credentials.json file.
                """
        flow = InstalledAppFlow.from_client_secrets_file(
            'C:\\Users\\crist\\PycharmProjects\\Facial_Recognition_System\\credentials2.json', self.SCOPES
        )
        creds = flow.run_local_server(port=8080)
        return creds

#Fetch data from view
    def fetch_course_schedule(self, professor_id, course_code,course_name, day_name):
        """
        Fetch the schedule for the given professor and course on a specific day.
        """
        query = """
        SELECT 
            professor_name, professor_email, course_name, day_name, start_time, end_time 
        FROM professor_course_schedule
        WHERE professor_id = % AND course_code = % AND day_name = %
        """
        #day_name = date.strftime('%A')  # Get the day name (e.g., Monday)
        self.connector.mycursor.execute(query, (professor_id, course_code,course_name, day_name))
        return self.connector.mycursor.fetchone()

    def fetch_attendance_report(self, course_code, date):
        """
        Fetch attendance data for the specified course and date.

        """
        query = """
        SELECT 
            student_name, course_name, attendance_date, attendance_status 
        FROM student_attendance_schedule 
        WHERE course_code = %s AND attendance_date = %s
        """
        self.connector.mycursor.execute(query, (course_code, date))
        return self.connector.mycursor.fetchall()
    """
    def send_email(self, professor_email, subject, body):
        Send an email with the attendance report.
        sender_email = 'jihcka@gmail.com'
        sender_password = 'PythonFall24'  #Creo que no es necesario

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = professor_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Use SMTP server for  email provider
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, professor_email, msg.as_string())
            server.quit()
            print(f"Report sent to {professor_email}")
        except Exception as e:
            print(f"Error sending email: {e}")
"""
    def send_email(self, professor_email, subject, body):
        """Send an email with the attendance report using Gmail's OAuth 2.0."""
        #SCOPES=['https://www.googleapis.com/auth/gmail.send']

        # If modifying the token file, delete the file to force reauthorization.
        #token_file = 'token.pickle'
        #creds = None
      #  if os.path.exists(token_file):
            #with open(token_file, 'rb') as token:
            #    creds = pickle.load(token)
                # If there are no (valid) credentials available, let the user log in.
            #if not creds or not creds.valid:
                #if creds and creds.expired and creds.refresh_token:
                   # creds.refresh(Request())
               # else:
                   # flow = InstalledAppFlow.from_client_secrets_file(
                      #  'credentials2.json', SCOPES)
                    #creds = flow.run_local_server(port=0)

                # Save the credentials for the next run
               # with open(token_file, 'wb') as token:
                    #pickle.dump(creds, token)
        creds=self.get_credentials()
        try:
            service = build('gmail', 'v1', credentials=creds)

            message = MIMEMultipart()
            message['From'] = 'jihcka@gmail.com'  # Your Gmail address
            message['To'] = professor_email
            message['Subject'] = subject

            message.attach(MIMEText(body, 'plain'))

            raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

            # Send the email
            message_sent = service.users().messages().send(userId="me", body=raw_message).execute()
            print(f"Report sent to {professor_email}, Message ID: {message_sent['id']}")
        except Exception as e:
            print(f"Error sending email: {e}")


    def generate_report_and_send_email(self, course_code, date):
        """Generate the report and send it to the professor's email."""
        attendance_data = self.fetch_attendance_report(course_code, date)

        if attendance_data:
            report_content = f"Attendance Report for Course: {course_code} on {date}\n\n"
            report_content += "Student name | Course Name | Attendance Date | Status\n"
            report_content += "-" * 80 + "\n"

            for row in attendance_data:
                print(row)
                report_content += f"{row[0]} | {row[1]} | {row[2]} | {row[3]} \n"

            professor_email = ("andrea130405@gmail.com")  # Change to retrieve the email from the database

            self.send_email(professor_email, f"Attendance Report for {course_code} on {date}", report_content)
        else:
            print(f"No attendance data found for course {course_code} on {date}")

    #Integrate Facial Recognition
    ############################
        #Method to call the generate report

        """
        def mark_attendance(self, student_id, course_code, course_name,status,date):
            #Mark attendance for the student in the given course.
            query = 
            
            
            #Verify the db values pq no me acuerdo como salian
            self.connector.mycursor.execute(query, (student_id, course_code, date))
            self.connector.connection_info.commit()
            print(f"Attendance marked for student {student_id} in course {course_code} on {date}")
        """


        #Query to specify in which course the attendance is being marked
        #Add group
        #
        def get_course_code(self, student_id, course_code,course_name,):
            """Get the course code for the student."""
            query = """
            SELECT course_code, course_name 
            FROM student_attendance_schedule 
            WHERE student_id = %s
            """
            self.connector.mycursor.execute(query, (student_id,))
            result = self.connector.mycursor.fetchone()
            return result[0] if result else None

    """def process_facial_recognition(self, recognized_faces, course_code, date):
        #Integrate facial recognition to mark attendance.
        for student_id in recognized_faces:
            self.mark_attendance(student_id, course_code, date)"""


class Attendance:
    def __init__(self):
        self.connector = Connector()
    def insert_attendance(self, student_id, schedule_id, attendance_date, status='Absent'):
        try:
            query="""
            INSERT INTO attendance (schedule_id,student_id,attendance_date, status)
            VALUES (%s, %s, %s, %s)
            """
            #Data to be inserted
            data=(schedule_id, student_id, attendance_date, status)
            self.connector.mycursor.execute(query, data)

            self.connector.connection_info.commit()
            print(f"Attendance for student {student_id} on attendance date {attendance_date} inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting attendance: {err}")
        finally:
            self.connector.mycursor.close()

