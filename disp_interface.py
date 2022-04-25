# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'disp_pic.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 290, 71, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 241, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 350, 71, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 241, 101))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 160, 241, 101))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 310, 71, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 10, 1280, 720))
        self.label.setAcceptDrops(True)
        self.label.setObjectName("label")

        self.label_mouse = QtWidgets.QLabel(self.centralwidget)
        self.label_mouse.setObjectName("mouse")
        self.label_mouse.setGeometry(QtCore.QRect(10, 400, 250, 40))
        self.label_mouse.setText("在图片上点击获取位置")
        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setObjectName("mouse")
        self.label_info.setGeometry(QtCore.QRect(10, 500, 250, 40))
        self.label_info.setText("显示信息")
        # self.label_mouse.adjustSize()
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(160, 270, 71, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(30, 330, 71, 31))
        self.pushButton_5.setObjectName("pushButton_5")
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
        self.pushButton.setText(_translate("MainWindow", "解析"))
        self.lineEdit.setText(_translate("MainWindow", "*: %f %f %f %f"))
        self.pushButton_2.setText(_translate("MainWindow", "画点"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">float : 0.5 0.5 0.1 0.1 0.75151 0.7455</p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">xywh : 0.6 0.6 0.2 0.2 0.75151 0.7455</p></body></html>"))
        self.textEdit_2.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">解析出来的点坐标</p></body></html>"))

        self.pushButton_3.setText(_translate("MainWindow", "连线"))
        self.pushButton_4.setText(_translate("MainWindow", "画矩形"))
        self.pushButton_5.setText(_translate("MainWindow", "还原"))
        # pixmap=QtGui.QPixmap("./image/draw_line_tmp.jpg")
        # self.label.setPixmap(pixmap.scaled(pic_label_width,pic_label_height,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        #self.label.setScaledContents(True)  # 让图片自适应label大小
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # 水平居中
        # self.label.setAcceptDrops(True)
        self.menuopen.setTitle(_translate("MainWindow", "open"))
        self.actionopen.setText(_translate("MainWindow", "open file"))
        self.actionopen.setShortcut(_translate("MainWindow", "Ctrl+O"))
# import source_pic
