# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'disp_pic.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from coord_trans import POINT_FORMAT

pic_label_width=1280
pic_label_height=720


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 800)
        MainWindow.setAcceptDrops(True)
        MainWindow.setStyleSheet("")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit_reg = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_reg.setGeometry(QtCore.QRect(10, 10, 241, 20))
        self.lineEdit_reg.setObjectName("lineEdit")

        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(10, 40, 241, 101))
        self.textEdit_log.setObjectName("textEdit_reg")
        self.textEdit_output_res = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_output_res.setGeometry(QtCore.QRect(10, 160, 241, 101))
        self.textEdit_output_res.setObjectName("textEdit_output_res")

        self.pushButton_restore = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_restore.setGeometry(QtCore.QRect(30, 330, 80, 30))

        self.pushButton_rect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_rect.setGeometry(QtCore.QRect(160, 270, 80, 30))
        self.pushButton_rect.setObjectName("pushButton_rect")
        self.pushButton_line = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_line.setGeometry(QtCore.QRect(160, 310, 80, 30))
        self.pushButton_line.setObjectName("pushButton_line")
        self.pushButton_point = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_point.setGeometry(QtCore.QRect(160, 350, 80, 30))
        self.pushButton_point.setObjectName("pushButton_point")
        self.pushButton_polygon = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_polygon.setGeometry(QtCore.QRect(160, 390, 80, 30))
        self.pushButton_polygon.setObjectName("pushButton_polygon")

        self.cb = QtWidgets.QComboBox(self)
        # 直接从枚举类中获取key list
        self.cb.addItems(list(POINT_FORMAT.__members__.keys()))
        self.cb.setGeometry(QtCore.QRect(10,450,120,30))
        # self.cb.move(10,450)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 10, 1280, 720))
        self.label.setAcceptDrops(True)
        self.label.setObjectName("label")

        self.label_mouse = QtWidgets.QLabel(self.centralwidget)
        self.label_mouse.setObjectName("mouse")
        self.label_mouse.setGeometry(QtCore.QRect(10, 600, 250, 40))
        self.label_mouse.setText("在图片上点击获取位置")
        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setObjectName("mouse")
        self.label_info.setGeometry(QtCore.QRect(10, 650, 250, 40))
        self.label_info.setText("显示信息")
        self.global_debug_info = QtWidgets.QLabel(self.centralwidget)
        self.global_debug_info.setObjectName("debug_info")
        self.global_debug_info.setGeometry(QtCore.QRect(10, 700, 250, 40))
        self.global_debug_info.setText("")
        # self.label_mouse.adjustSize()


        # self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        # self.horizontalSlider.setGeometry(QtCore.QRect(290, 480, 731, 22))
        # self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        # self.horizontalSlider.setObjectName("horizontalSlider")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1052, 23))
        self.menubar.setObjectName("menubar")
        self.menuopen = QtWidgets.QMenu(self.menubar)
        self.menuopen.setObjectName("menuopen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.menuopen.addAction(self.actionopen)
        self.menubar.addAction(self.menuopen.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_reg.setText(_translate("MainWindow", "*: %f %f %f %f"))
        self.pushButton_point.setText(_translate("MainWindow", "画点"))
        self.textEdit_log.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'SimSun\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">float : 0.5 0.5 0.1 0.1 0.75151 0.7455</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">xywh : 0.6 0.6 0.2 0.2 0.75151 0.7455</p></body></html>"))
        self.textEdit_output_res.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'SimSun\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">解析出来的点坐标</p></body></html>"))

        self.pushButton_line.setText(_translate("MainWindow", "画线"))
        self.pushButton_rect.setText(_translate("MainWindow", "画矩形"))
        self.pushButton_restore.setText(_translate("MainWindow", "还原"))
        self.pushButton_polygon.setText(_translate("MainWindow","画多边形"))
        # pixmap=QtGui.QPixmap("./image/draw_line_tmp.jpg")
        # self.label.setPixmap(pixmap.scaled(pic_label_width,pic_label_height,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        #self.label.setScaledContents(True)  # 让图片自适应label大小
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # 水平居中
        # self.label.setAcceptDrops(True)
        self.menuopen.setTitle(_translate("MainWindow", "open"))
        self.actionopen.setText(_translate("MainWindow", "open file"))
        self.actionopen.setShortcut(_translate("MainWindow", "Ctrl+O"))
# import source_pic
