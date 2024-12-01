# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)
from PySide6.QtCore import QThread, Signal, Slot
import cv2
import numpy as np
from FaceRecognition.Live_face_detection import CameraDetector


class Ui_Camera(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 540)
        Form.setMinimumSize(QSize(640, 540))
        Form.setMaximumSize(QSize(640, 540))
        self.camera_image = QLabel(Form)
        self.camera_image.setObjectName(u"camera_image")
        self.camera_image.setGeometry(QRect(20, 30, 591, 421))
        self.take_photo_btn = QPushButton(Form)
        self.take_photo_btn.setObjectName(u"take_photo_btn")
        self.take_photo_btn.setGeometry(QRect(200, 480, 221, 41))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.take_photo_btn.setFont(font)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.camera_image.setText("")
        self.take_photo_btn.setText(QCoreApplication.translate("Form", u"Take group photo", None))
    # retranslateUi

class MyThread(QThread):
    frame_signal = Signal(QImage)
    photo_captured_signal = Signal(QImage)
    faces_signal = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.camera_detector = None

    def run(self):
        """Creates a new camera object. Base code provided by Medium at:
        https://medium.com/@ilias.info.tel/display-opencv-camera-on-a-pyqt-app-4465398546f7"""
        cap = cv2.VideoCapture(0)
        def process_frame_callback(qt_image):
            self.frame_signal.emit(qt_image)

        self.camera_detector = CameraDetector(cap, process_frame_callback)
        if cap.isOpened():
            self.camera_detector.start_camera(cap)

    def take_photo(self):
        """Freezes into the last frame and sends the faces captured to the main window."""
        if self.camera_detector:
            frame, faces = self.camera_detector.stop_and_capture()
            self.faces_signal.emit(faces)
            if frame is not None:
                self.photo_captured_signal.emit(frame)
            self.camera_detector.running = False  # Ensure threads stop
            self.camera_detector = None

    def stop(self):
        self.running = False
        if self.camera_detector:
            self.camera_detector.running = False  # Stop the camera detector threads
        self.wait()


class QWidgetCamera(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Camera()
        self.ui.setupUi(self)
        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)
        self.ui.take_photo_btn.clicked.connect(self.take_photo)


    def open_camera(self):
        self.camera_thread.start()

    def take_photo(self):
        if self.camera_thread:
            self.camera_thread.take_photo()
            self.destroy()

    @Slot(QImage)
    def setImage(self, image):
        self.ui.camera_image.setPixmap(QPixmap.fromImage(image))



