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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget
import cv2
import imutils
from FaceRecognition.Live_face_detection import CameraDetector
from FaceRecognition.face_Recognition_Training import trainer_main

class Ui_Camera(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 480)
        Form.setMinimumSize(QSize(640, 480))
        Form.setMaximumSize(QSize(640, 480))
        self.camera_image = QLabel(Form)
        self.camera_image.setObjectName(u"camera_image")
        self.camera_image.setGeometry(QRect(20, 30, 591, 421))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.camera_image.setText("")
    
# This Python file uses the following encoding: utf-8

class MyThread(QThread):
    frame_signal = Signal(QImage)

    def __init__(self, camera_index=0, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        #trainer_main()
        cap = cv2.VideoCapture(0)

        def process_frame_callback(qt_image):
            self.frame_signal.emit(qt_image)

        camera_detection = CameraDetector(cap, process_frame_callback)
        if cap.isOpened():
            camera_detection.start_camera(cap)
            pass


# Camera widget class
class QWidgetCamera(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Camera()
        self.ui.setupUi(self)
        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)

    def open_camera(self):
        self.camera_thread.start()

    @Slot(QImage)
    def setImage(self, image):
        self.ui.camera_image.setPixmap(QPixmap.fromImage(image))