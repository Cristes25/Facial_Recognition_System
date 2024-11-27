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
from ui_camera import QWidgetCamera
import sys

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
        self.ui.takeAttendance_btn.clicked.connect(self.open_widget)

    def show_main_window(self):
        # Show the main window again after the child window is closed
        self.show()

    def open_widget(self):
        self.hide()
        self.child_window = QWidgetCamera()
        self.child_window.show()
        self.child_window.open_camera()
        self.child_window.destroyed.connect(self.show_main_window)
        self.ui.report_btn.setEnabled(True)

    # def cargarCombobox(self):
    #     try:
    #         listaRegiones = self.dtu.listaRegiones()
    #         self.ui.cbox_cod_region.addItem("Region*")
    #         for region in listaRegiones:
    #             self.ui.cbox_cod_region.addItem(str(region._region_name), str(region._region_id))
    #     except Exception as e:
    #         print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
