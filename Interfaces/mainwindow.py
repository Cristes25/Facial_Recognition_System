# This Python file uses the following encoding: utf-8
import sys
from camera import QWidgetCamera
from PyQt5 import uic
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui")
        self.takeAttendance_btn = self.findChild(QPushButton, "takeAttendance_btn")
        self.takeAttendance_btn.clicked.connect(self.open_widget)

    def open_widget(self):
        self.child_window = QWidgetCamera()
        self.child_window.show()


