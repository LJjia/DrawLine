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

import sys, shutil ,os ,pickle
from enum import Enum
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider
from PyQt5 import QtGui, QtCore
from coord_trans import POINT_FORMAT,POINT_VALUE, abs_convert_normal
import coord_trans
from disp_interface import Ui_MainWindow, pic_label_width, pic_label_height
import draw_line_func
import get_xy_pos
import yuvAnly
import read_yuv


disp_yuv_tmp_path = './image/draw_line_tmp_yuv.jpg'
disp_file_path = './image/draw_line_tmp.jpg'
disp_file_path_backup = './image/draw_line_tmp_backup.jpg'

class SAVE_DICTKEY_INFO(Enum):
    '''
    description: 保存的字典关键字名称
    param {*}
    return {*}
    '''    
    input_log=0,
    regulation_str=1,




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
        self.pushButton_point.clicked.connect(self.draw_point)
        self.pushButton_line.clicked.connect(self.draw_line)
        self.pushButton_rect.clicked.connect(self.draw_rectangle)
        self.pushButton_restore.clicked.connect(self.restore)
        self.pushButton_polygon.clicked.connect(self.draw_polygon)
        self.cb.currentIndexChanged[str].connect(self.proc_combox)
        self.actionopen.triggered.connect(self.open_file)
        # 初始化一些全局变量
        self.source_file_path = disp_file_path
        self.source_file_path_backup = disp_file_path_backup
        self.source_yuv_path_backup = disp_yuv_tmp_path
        self.disp_pic_info(self.source_file_path)
        self.file_path = './test/test_img.jpg'
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
        self.input_dict={}
        self.input_dict_dir="./image/input_param.pkl"
        if os.path.exists(self.input_dict_dir):
            # 记忆模式,保存上次的结果
            with open(self.input_dict_dir, 'rb') as f:
                dict_tmp = pickle.load(f)
                assert isinstance(dict_tmp,dict)
                if SAVE_DICTKEY_INFO.input_log.name in dict_tmp:
                    self.textEdit_log.setText(dict_tmp[SAVE_DICTKEY_INFO.input_log.name])
                if SAVE_DICTKEY_INFO.regulation_str.name in dict_tmp:
                    self.lineEdit_reg.setText(dict_tmp[SAVE_DICTKEY_INFO.regulation_str.name])

        # 输入点位格式
        # 为了和选择的统一,先迭代出第一个
        self.point_pos_format = iter(POINT_FORMAT).__next__()

        # 进度条规则
        # 值修改不做绑定
        # self.video_cur_pos = self.horizontalSlider.value()
        # # self.horizontalSlider.valueChanged.connect(self.drag_slider)
        # self.horizontalSlider.sliderReleased.connect(self.drag_confirm)
        # self.horizontalSlider.setTickPosition(QSlider.TicksBelow)#设置刻度位置，在下方
        # self.horizontalSlider.setMaximum(400)

    def proc_combox(self,in_str):
        # 修改type类型
        self.point_pos_format=eval("POINT_FORMAT.%s"%(in_str))


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

    def set_debug_msg(self,msg):
        if(not isinstance(msg,str)):
            return
        self.global_debug_info.setStyleSheet("color:red")
        self.global_debug_info.setText(msg)

    def clear_debug_msg(self):
        self.global_debug_info.setText("")

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

    def disp_pic_info(self,file_path=""):
        if(not file_path):
            file_path=self.source_file_path
        if not os.path.exists(file_path):
            return
        w, h = draw_line_func.get_pic_param(file_path)
        self.pic_wh = [w, h]
        pic_info_text = "图片宽:%s 高%s" % (self.pic_wh[0], self.pic_wh[1])
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

    def save_input_log(self,intput_log,re_exp):
        # 保存临时字典
        with open(self.input_dict_dir, 'wb') as f:
            param_dict = {
                SAVE_DICTKEY_INFO.input_log.name: intput_log,
                SAVE_DICTKEY_INFO.regulation_str.name: re_exp,
            }
            pickle.dump(param_dict, f)

    def parse_rect_format(self,format):
        print("parse result ")
        regulation_str = self.lineEdit_reg.text()
        input_log = self.textEdit_log.toPlainText()
        outputPosition_list = get_xy_pos.parse_file(input_log, regulation_str)
        self.disp_pic_info()
        print(outputPosition_list)
        for i in range(len(outputPosition_list)):
            if max(outputPosition_list[i])>1:
                # 证明给的点是绝对坐标值,这里转化为归一化坐标
                outputPosition_list[i]=abs_convert_normal(outputPosition_list[i],self.pic_wh[0],self.pic_wh[1])
        # 针对 其他点集皆转化为xywh格式做特殊处理
        if (format != POINT_FORMAT.XYWH):
            for i in range(len(outputPosition_list)):
                outputPosition_list[i] = coord_trans.rect_point_format_trans(outputPosition_list[i],
                                                                             format,
                                                                             POINT_FORMAT.XYWH)
        # 打印str
        outputPosition_disp = ""
        for point in outputPosition_list:
            outputPosition_disp += "{pos}\n".format(pos=point)
        self.textEdit_output_res.setText(outputPosition_disp)
        self.save_input_log()
        print("解析出来列表", outputPosition_list)
        # 返回list
        return outputPosition_list

    def draw_rectangle(self):
        rect_enum=[POINT_FORMAT.XYWH,POINT_FORMAT.CXYWH,POINT_FORMAT.X1X2Y1Y2,POINT_FORMAT.X1Y1X2Y2]
        if(self.point_pos_format not in rect_enum):
            self.set_debug_msg("%s not rect format"%(self.point_pos_format.name))
            return
        outputPosition_list=self.parse_rect_format(self.point_pos_format)
        if not self.check_format(outputPosition_list, 'rectangle'):
            self.set_debug_msg("parse str res not rect format!")
            return

        draw_line_func.draw_rectangle(self.source_file_path, outputPosition_list, color='red', pixel_size=4)
        self.setSuitPicDisp(self.source_file_path)
        # 实例显示QApplication.processEvents()这个函数放在画矩形函数最后面没什么用
        # QApplication.processEvents()
        return self.clear_debug_msg()


    def parse_line_format(self):
        print("parse result ")
        regulation_str = self.lineEdit_reg.text()
        input_log = self.textEdit_log.toPlainText()
        outputPosition_list = get_xy_pos.parse_file(input_log, regulation_str)
        self.disp_pic_info()
        print(outputPosition_list)
        for i in range(len(outputPosition_list)):
            if max(outputPosition_list[i]) > 1:
                # 证明给的点是绝对坐标值,这里转化为归一化坐标
                outputPosition_list[i] = abs_convert_normal(outputPosition_list[i], self.pic_wh[0], self.pic_wh[1])
        # 打印str
        outputPosition_disp = ""
        for point in outputPosition_list:
            outputPosition_disp += "{pos}\n".format(pos=point)
        self.textEdit_output_res.setText(outputPosition_disp)
        # 保存临时字典
        self.save_input_log()
        print("解析出来列表", outputPosition_list)
        # 返回list
        return outputPosition_list

    def draw_line(self):
        line_enum = [POINT_FORMAT.XY_LIST]
        if (self.point_pos_format not in line_enum):
            self.set_debug_msg("%s not rect format" % (self.point_pos_format.name))
            return
        outputPosition_list = self.parse_line_format()
        if not self.check_format(outputPosition_list, 'line'):
            self.set_debug_msg("parse str res not line format!")
            return
        draw_line_func.draw_line(self.source_file_path, outputPosition_list, color='red', pixel_size=4)
        self.setSuitPicDisp(self.source_file_path)
        return self.clear_debug_msg()

    def parse_point_format(self):
        print("parse result ")
        regulation_str = self.lineEdit_reg.text()
        input_log = self.textEdit_log.toPlainText()
        outputPosition_list = get_xy_pos.parse_file(input_log, regulation_str)
        self.disp_pic_info()
        print(outputPosition_list)
        for i in range(len(outputPosition_list)):
            if max(outputPosition_list[i]) > 1:
                # 证明给的点是绝对坐标值,这里转化为归一化坐标
                outputPosition_list[i] = abs_convert_normal(outputPosition_list[i], self.pic_wh[0], self.pic_wh[1])
        # 打印str
        outputPosition_disp = ""
        for point in outputPosition_list:
            outputPosition_disp += "{pos}\n".format(pos=point)
        self.textEdit_output_res.setText(outputPosition_disp)
        # 保存临时字典
        self.save_input_log()
        print("解析出来列表", outputPosition_list)
        # 返回list
        return outputPosition_list

    def draw_point(self):
        point_enum = [POINT_FORMAT.XY_LIST,POINT_FORMAT.XY]
        if (self.point_pos_format not in point_enum):
            self.set_debug_msg("%s not point format" % (self.point_pos_format.name))
            return
        outputPosition_list = self.parse_line_format()
        if not self.check_format(outputPosition_list, 'point'):
            self.set_debug_msg("parse str res not line format!")
            return
        draw_line_func.draw_point(self.source_file_path, outputPosition_list, color='red', pixel_size=6)
        self.setSuitPicDisp(self.source_file_path)
        return self.clear_debug_msg()


    def parse_polygon_format(self):
        regulation_str = self.lineEdit_reg.text()
        input_log = self.textEdit_log.toPlainText()
        outputPosition_list = get_xy_pos.parse_file(input_log, regulation_str)
        self.disp_pic_info()
        print(outputPosition_list)
        for i in range(len(outputPosition_list)):
            if max(outputPosition_list[i]) > 1:
                # 证明给的点是绝对坐标值,这里转化为归一化坐标
                outputPosition_list[i] = abs_convert_normal(outputPosition_list[i], self.pic_wh[0], self.pic_wh[1])
        # 打印str
        outputPosition_disp = ""
        for point in outputPosition_list:
            outputPosition_disp += "{pos}\n".format(pos=point)
        self.textEdit_output_res.setText(outputPosition_disp)
        # 保存临时字典
        self.save_input_log()
        print("解析出来列表", outputPosition_list)
        # 返回list
        return outputPosition_list

    def draw_polygon(self):
        point_enum = [POINT_FORMAT.XY_LIST]
        if (self.point_pos_format not in point_enum):
            self.set_debug_msg("%s not point format" % (self.point_pos_format.name))
            return
        outputPosition_list = self.parse_line_format()
        if not self.check_format(outputPosition_list, 'point'):
            self.set_debug_msg("parse str res not line format!")
            return
        draw_line_func.draw_polygon(self.source_file_path, outputPosition_list, color='red', pixel_size=6)
        self.setSuitPicDisp(self.source_file_path)
        return self.clear_debug_msg()

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
