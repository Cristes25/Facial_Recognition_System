# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

from Attendance_Report_Generation import Attendance, AttendanceReportGenerator
from database_connection import Connector
from ui_camera import QWidgetCamera
# from Attendance_Report_Generation import
import sys
import datetime

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 220)
        MainWindow.setMinimumSize(QSize(400, 220))
        MainWindow.setMaximumSize(QSize(400, 220))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(9, 100, 381, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.takeAttendance_btn = QPushButton(self.horizontalLayoutWidget)
        self.takeAttendance_btn.setObjectName(u"takeAttendance_btn")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.takeAttendance_btn.setFont(font)

        self.horizontalLayout.addWidget(self.takeAttendance_btn)

        self.report_btn = QPushButton(self.horizontalLayoutWidget)
        self.report_btn.setObjectName(u"report_btn")
        self.report_btn.setFont(font)
        self.report_btn.setEnabled(False)  # Initially disable the button

        self.horizontalLayout.addWidget(self.report_btn)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 10, 181, 20))
        self.label.setFont(font)
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(11, 50, 381, 28))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 400, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.takeAttendance_btn.setText(QCoreApplication.translate("MainWindow", u"Take attendance", None))
        self.report_btn.setText(QCoreApplication.translate("MainWindow", u"Generate report", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Choose a course", None))
    # retranslateUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.takeAttendance_btn.clicked.connect(self.open_attendance)
        self.ui.report_btn.clicked.connect(self.generate_report)
        self.students = []
        self.connection = Connector()
        self.fill_Combobox()

    def show_main_window(self):
        # Show the main window again after the child window is closed
        self.show()
        self.ui.report_btn.setEnabled(False)

    def open_attendance(self):
        self.hide()
        self.child_window = QWidgetCamera()
        self.child_window.show()
        self.child_window.open_camera()
        self.child_window.camera_thread.faces_signal.connect(lambda data: self.store_faces(data))

    def store_faces(self, faces):
        self.ui.comboBox.setEditable(False)
        self.show()
        self.ui.report_btn.setEnabled(True)
        self.students = [] # Clean it in case the program runs multiple times
        for id in faces:
            self.students.append(int(id))

    def fill_Combobox(self):
        try:
            # current_day = datetime.datetime.now().strftime("%A")
            # current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_day = 'Monday'
            current_time = '09:14:00'
            data = (current_day, current_time)
            current_classes = self.connection.get_schedule_id(data)
            for row in current_classes:
                self.ui.comboBox.addItem(f"Group {row[1]} | {row[2]} {row[3]}", (row[0], row[2]))
        except Exception as e:
            print(e)

    def generate_report(self):
        attendance = Attendance()
        date = datetime.date.today()
        data = self.ui.comboBox.currentData()
        schedule_id = data[0]
        course_id = data[1]
        for student in self.students:
            attendance.insert_attendance(student, schedule_id,  date, 'Present')
        self.ui.comboBox.setEditable(True)
        attendance_report = AttendanceReportGenerator()
        attendance_report.generate_report_and_send_email(course_code=course_id, date=str(date))
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
