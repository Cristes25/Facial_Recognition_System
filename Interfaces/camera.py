# This Python file uses the following encoding: utf-8

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QThread,pyqtSignal as Signal,pyqtSlot as Slot
import cv2,imutils

class MyThread(QThread):
    frame_signal = Signal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            _, frame = self.cap.read()
            frame = self.cvimage_to_label(frame)
            self.frame_signal.emit(frame)

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(
            image,
            image.shape[1],
            image.shape[0],
            QImage.Format_RGB888
        )
        return image

# Camera widget class
class QWidgetCamera(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("camera.ui")
        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)

    def open_camera(self):
        self.camera_thread.start()

    @Slot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
