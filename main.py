#!/usr/bin/env python
# -*- coding:utf-8 _*-
__author__ = 'LJjia'
# *******************************************************************
#     Filename @    main.py.py
#       Author @    Jia LiangJun
#  Create date @    2020/5/10 20:43
#        Email @    LJjiahf@163.com
#  Description @    调用显示界面主函数
# ********************************************************************

import sys, shutil
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider
from PyQt5 import QtGui, QtCore
from coord_trans import POINT_FORMAT,POINT_VALUE, abs_convert_normal
import coord_trans
from disp_interface import Ui_MainWindow, pic_label_width, pic_label_height
import draw_line_func
import GetXYPos
import os
import yuvAnly
import read_yuv


disp_yuv_tmp_path = './image/draw_line_tmp_yuv.jpg'
disp_file_path = './image/draw_line_tmp.jpg'
disp_file_path_backup = './image/draw_line_tmp_backup.jpg'



class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 先要开启父类的鼠标跟踪事件,子类的鼠标跟踪事件擦除能开启
        self.centralWidget().setMouseTracking(True)
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.label.installEventFilter(self.label)
        # 设置信号的绑定关系
        self.pushButton.clicked.connect(self.input_param_parse)
        self.pushButton_2.clicked.connect(self.draw_point)
        self.pushButton_3.clicked.connect(self.draw_line)
        self.pushButton_4.clicked.connect(self.draw_rectangle)
        self.pushButton_5.clicked.connect(self.restore)
        self.actionopen.triggered.connect(self.open_file)
        # 初始化一些全局变量
        self.source_file_path = disp_file_path
        self.source_file_path_backup = disp_file_path_backup
        self.source_yuv_path_backup = disp_yuv_tmp_path
        self.regulation_str = ""
        self.input_log = ""
        self.outputPosition = []
        self.file_path = './test/test_img.jpg'
        # 是否爬取过参数,每次画线前要先检查
        self.ifParserParam = 0
        self.setAcceptDrops(True)
        # 设置进度条,这部分属于视频解码的内容
        # 分别为,视频总长,当前滑块在slider中的位置,确定需要解码的位置
        self.video_total_len = 0
        self.slider_cur_pos = 0
        self.decode_pos = 0
        self.scale_pic_width = 0
        self.scale_pic_height = 0
        self.pic_wh=[0,0]
        self.yuvAnlyer = yuvAnly.YuvAnlysiser()
        if not os.path.exists("./image"):
            os.makedirs("./image")
        if os.path.exists(self.source_file_path):
            self.setSuitPicDisp(self.source_file_path)

        # some define and point format

        # self.XYWH_TO_X1X2Y1Y2='xywh_2_x1x2y1y2'
        # 
        # self.POINT_FORMAT_XYWH = 'point_format_xywh'
        # self.POINT_FORMAT_X1X2Y1Y2 = 'point_format_x1x2y1y2'
        # self.POINT_FORMAT_XY_LIST = 'point_format_xy_list'

        # 输入点位格式 默认xywh
        self.point_pos_format = POINT_FORMAT.XYWH

        # 进度条规则
        # 值修改不做绑定
        # self.video_cur_pos = self.horizontalSlider.value()
        # # self.horizontalSlider.valueChanged.connect(self.drag_slider)
        # self.horizontalSlider.sliderReleased.connect(self.drag_confirm)
        # self.horizontalSlider.setTickPosition(QSlider.TicksBelow)#设置刻度位置，在下方
        # self.horizontalSlider.setMaximum(400)

    def calc_normal_value_in_pic(self,x,y):
        '''
        获取点击位置在图片上的绝对坐标
        :param x:
        :param y:
        :param offset_x:
        :param offset_y:
        :return:
        '''

        label_x=int(self.label.geometry().x())
        label_y = int(self.label.geometry().y())
        label_width=int(self.label.geometry().width())
        label_height = int(self.label.geometry().height())
        label_center_x=(label_x+label_width)/2
        label_center_y = (label_y + label_height) / 2
        band_left=int((label_width-self.scale_pic_width)/2)
        band_up = int((label_height - self.scale_pic_height) / 2)
        print("click x y %s %s"%(x,y),band_left,band_up,label_width,label_height,self.scale_pic_width,self.scale_pic_height)
        if(x>=label_center_x-self.scale_pic_width/2 and x<=label_center_x+self.scale_pic_width/2)and\
                (y>=label_center_y-self.scale_pic_height/2 and y<=label_center_y+self.scale_pic_height/2):
            click_x=x-band_left-label_x
            click_y=y-band_up-label_y
            print('after calc',click_x,click_y)
            nor_x=click_x/self.scale_pic_width
            nor_y = click_y / self.scale_pic_height
            return (nor_x,nor_y)
        else:
            return (-1,-1)


    def mousePressEvent(self, event):
        # 尝试按住拖动时是否会打印
        x = event.x()
        y = event.y()
        (value_x,value_y)=self.calc_normal_value_in_pic(x,y)
        if value_x==-1:
            return
        text = "点击位置 x:%.2f,y:%.2f"%(value_x, value_y)
        print(text)
        self.label_mouse.setText(text)

    def check_format(self, data_list, format):
        if format == 'rectangle':
            # 矩形类型[(x1,y1,w1,h1),(x2,y2,w2,h2)]
            if len(data_list) > 0:
                if len(data_list[0]) == 4:
                    return True
                else:
                    return False
        if format == 'line' or format == 'point':
            # 线,点类型[(x1,y1),(x2,y2)]
            if len(data_list) > 0:
                if len(data_list[0]) == 2:
                    return True
                else:
                    return False

    def setSuitPicDisp(self, file_path):
        '''
        设置合适的宽高比显示
        '''
        # pixmap=QtGui.QPixmap(self.source_file_path)
        scale_map = QtGui.QPixmap(self.source_file_path).scaled(pic_label_width, pic_label_height,
                                                                QtCore.Qt.KeepAspectRatio,
                                                                QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(scale_map)
        self.scale_pic_width= scale_map.width()
        self.scale_pic_height= scale_map.height()


    def file_copy_and_disp(self, file_path):
        '''
        文件拷贝和显示
        :return:
        '''
        # 这个函数最像linux下的cp命令了
        draw_line_func.convert_file_type_to_jpeg(file_path, self.source_file_path)
        draw_line_func.convert_file_type_to_jpeg(file_path, self.source_file_path_backup)
        self.setSuitPicDisp(self.source_file_path)
        w,h=draw_line_func.get_pic_param(self.source_file_path)
        self.pic_wh=[w,h]
        pic_info_text="图片宽:%s 高%s"%(self.pic_wh[0],self.pic_wh[1])
        self.label_info.setText(pic_info_text)

    def dragEnterEvent(self, e):
        '''
        重写拖拽函数,原来的函数是空.当拖曳操作在其目标控件上被被拖入时，这个事件将被触发,默认接受,详情看MIME类型的拖拽数据传输
        :param e:
        :return:
        '''
        e.accept()

    def dropEvent(self, e):
        '''
        当拖曳操作在其目标控件上被释放时，这个事件将被触发,详情看MIME类型的拖曳数据传输
        :param e:
        :return:
        '''
        # 添加拖曳文本到条目中
        file_path = e.mimeData().text()
        print("get file ", file_path)
        if(sys.platform=="darwin"):
            # mac
            file_path_prefix='file://'
        elif (sys.platform=='win32'):
            # windows
            file_path_prefix = 'file:///'
        else:
            # 其他linux
            file_path_prefix = 'file://'

        # Mac和linux上目录第一个字符带/User... window直接是C:/ 所以Mac上是file://替换
        if 0 == file_path.find(file_path_prefix):
            # 如果file_path的开头位置是字符串'file:///',将其替换为空
            # find 返回第一次发现字符串的位置
            file_path = file_path.replace(file_path_prefix, '')

        self.file_path = file_path
        # 检测是否为yuv图片
        ret ,_= read_yuv.sniff_head(file_path)
        if ret > 0:
            # 检测为自定义yuv图片成功
            print("find yuv data check head ok datalen %s" % ret)
            self.yuvAnlyer.anlysis_yuv_frame(file_path, save_path=self.source_yuv_path_backup)
            # 下面处理特殊,yuv直接保存意义不大,将yuv转换成jpeg后在拷贝至本地,替换掉self.file_path这个变量
            self.file_path = self.source_yuv_path_backup
        pic_info_text = "拖拽图片!"
        self.label_info.setText(pic_info_text)
        # 不是带后缀的yuv则按照支持的jpeg png 等图片流程走
        self.file_copy_and_disp(self.file_path)

    def open_file(self):
        # 第一个参数制定窗口标题 ,后面的分别为 默认寻找的路径 文件名过滤器 ...()
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", ".",
                                                         "All Files (*);;JPEG File (*.jpg;*.jpeg);;PNG File(*.png)")
        print(fileName, filetype)
        self.file_path = fileName
        self.file_copy_and_disp(self.file_path)

    def restore(self):
        shutil.copy(self.source_file_path_backup, self.source_file_path)
        self.setSuitPicDisp(self.source_file_path)

    def point_format_trans(self,point,src_format,dst_format):
        # param check
        if len(point)!=4:
            print("func point_format_trans param error %s"%point)
        if src_format==self.POINT_FORMAT.XYWH and dst_format==self.POINT_FORMAT.X1X2Y1Y2:
            return (point[0],point[0]+point[2],point[1],point[1]+point[3])
        if src_format==self.POINT_FORMAT.X1X2Y1Y2 and dst_format==self.POINT_FORMAT.XYWH:
            return (point[0],point[1],point[1]-point[0],point[3]-point[2])


    def input_param_parse(self):
        # 获取和设置输入文本内容
        self.regulation_str = self.lineEdit.text()
        self.input_log = self.textEdit.toPlainText()
        outputPosition_list = GetXYPos.parse_file(self.input_log, self.regulation_str)
        if max(self.pic_wh)==0:
            w,h=draw_line_func.get_pic_param(self.source_file_path)
            self.pic_wh=[w,h]
        print("parse config file",outputPosition_list)

        for i in range(len(outputPosition_list)):
            if max(outputPosition_list[i])>1:
                # 证明给的点是绝对坐标值,这里转化为归一化坐标
                outputPosition_list[i]=abs_convert_normal(outputPosition_list[i],self.pic_wh[0],self.pic_wh[1])

        # 针对 x1x2y1y2做特殊处理
        if(self.point_pos_format==POINT_FORMAT.X1X2Y1Y2):
            for i in range(len(outputPosition_list)):
                outputPosition_list[i]=coord_trans.rect_point_format_trans(outputPosition_list[i],POINT_FORMAT.X1X2Y1Y2,POINT_FORMAT.XYWH)
                

        outputPosition_disp = ""
        for point in outputPosition_list:
            outputPosition_disp += "{pos}\n".format(pos=point)
        self.outputPosition = outputPosition_list
        self.textEdit_2.setText(outputPosition_disp)
        print("解析出来列表", outputPosition_list)
        self.ifParserParam = 1

    def draw_rectangle(self):
        if not self.ifParserParam:
            self.input_param_parse()
        if not self.check_format(self.outputPosition, 'rectangle'):
            return
        # 保存的路径和self.source_file_path一样,在draw_line_func中设置的
        draw_line_func.draw_rectangle(self.source_file_path, self.outputPosition, color='red', pixel_size=4)
        # 实例显示QApplication.processEvents()这个函数放在画矩形函数最后面没什么用
        # 不如直接显示设置label的属性
        self.setSuitPicDisp(self.source_file_path)
        self.ifParserParam = 0
        # QApplication.processEvents()

    def draw_line(self):
        if not self.check_format(self.outputPosition, 'line'):
            return
        draw_line_func.draw_line(self.source_file_path, self.outputPosition, color='red', pixel_size=4)
        self.setSuitPicDisp(self.source_file_path)
        self.ifParserParam = 0

    def draw_point(self):
        if not self.check_format(self.outputPosition, 'point'):
            return
        draw_line_func.draw_point(self.source_file_path, self.outputPosition, color='red', pixel_size=4)
        self.setSuitPicDisp(self.source_file_path)
        self.ifParserParam = 0

    # def drag_slider(self,value):
    #     '''
    #     拖拽进度条,切换不同的视频图片
    #     :return:
    #     '''
    #     self.slider_cur_pos = value

    def drag_confirm(self):
        '''
        拖拽进度条,释放的时候调用
        :return:
        '''
        self.decode_pos = self.horizontalSlider.value()
        print("confirm value ", self.decode_pos)


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 保证图片实时刷新
    QApplication.processEvents()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())

# "x":$,"y":$,"width":$,"height":$
