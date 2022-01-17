#!/usr/bin/env python
# -*- coding:utf-8 _*-
__author__ = 'LJjia'
# *******************************************************************
#     Filename @    yuvAnly.py
#       Author @    Jia LiangJun
#  Create date @    2020/10/14 22:18
#        Email @    LJjiahf@163.com
#  Description @    直接从yuv数据中读取信息,需要写入时写入 对应结构体
# ********************************************************************


import cv2
import numpy as np
import os
import read_yuv

yuv_file_path = './yuvdata'


class YuvAnlysiser():
    '''
    yuv 数据分析类
    '''

    def __init__(self):
        self.cv_font = cv2.FONT_HERSHEY_PLAIN
        self.cv_red = (0, 0, 255)
        self.cv_green = (0, 0, 255)
        # 文字每次偏移量
        self.txt_offser = 18
        self.font_width = 2
        self.font_size = 1.4
        # 线宽 默认2
        self.line_width = 2

    def __del__(self):
        pass

    def draw_on_img(self, width, height, obj_num, obj_list, img):
        '''
        cv 图片上画线
        :param width:
        :param height:
        :param obj_num:
        :param obj_list:
        :param img:
        :return:
        '''

        # draw obj rect
        for obj_name in obj_list.keys():
            if obj_name=='obj_num':
                continue
            obj_info=obj_list[obj_name]
            y_pos = 0
            start_x = int(width * obj_info["rect"][0])
            start_y = int(height * obj_info["rect"][1])
            end_x = int(
                width * obj_info["rect"][0] + width * obj_info["rect"][2])
            end_y = int(
                height * obj_info["rect"][1] + height * obj_info["rect"][3])

            cv2.rectangle(img, (start_x, start_y), (end_x, end_y), self.cv_red, self.line_width)
            # 如果id为0则不显示
            if obj_info["id"] != 0:
                cv2.putText(img, 'ID:%d' % (obj_info["id"]), (start_x, start_y + y_pos),
                            self.cv_font, self.font_size, self.cv_green, self.font_width)
                y_pos += self.txt_offser
            # socrelist 是float 类型的list 没有多余维度
            if obj_info["score"] != 0:
                cv2.putText(img, 'sco:%.2f' % (obj_info["score"]), (start_x, start_y + y_pos),
                            self.cv_font, self.font_size, self.cv_green, self.font_width)
                y_pos += self.txt_offser

            if obj_info["confindence"] != 0:
                cv2.putText(img, 'con:%.2f' % (obj_info["confindence"]),
                            (start_x, start_y + y_pos),
                            self.cv_font, self.font_size, self.cv_green, self.font_width)
                y_pos += self.txt_offser

            # draw attr label
            for attr_name in obj_info["attr_list"].keys():
                if attr_name =='attr_num':
                    continue
                attr_info=obj_info["attr_list"][attr_name]
                if attr_name != '':
                    cv2.putText(img,
                                '%s L:%d Conf:%.3f' % (
                                    # desc
                                    attr_name,
                                    # label
                                    attr_info['label'],
                                    # condfidence
                                    attr_info['confindence']),
                                (start_x, start_y + y_pos),
                                self.cv_font, self.font_size, self.cv_green, self.font_width)
                else:
                    cv2.putText(img,
                                'UnknowAttr: L:%d Conf:%.3f' % (
                                    # label
                                    attr_info['label'],
                                    # condfidence
                                    attr_info['confindence']),
                                (start_x, start_y + y_pos),
                                self.cv_font, self.font_size, self.cv_green, self.font_width)
                y_pos += self.txt_offser

        # draw 规则
        #
        #   用不到,暂未实现
        #

    def anlysis_yuv_frame(self, filename, out_img=False, save_path=None):
        '''
        显示一帧的yuv图像
        :param filename:yuv文件名
        :param width:yuv图像宽
        :param height:yuv图像高
        :return:
        '''
        fp = open(filename, 'rb')
        param_dict = read_yuv.parse_yuv_info(fp)
        if -1 == param_dict:
            return
        width = param_dict['w']
        stride = param_dict['stride']
        height = param_dict['h']
        # print(param_dict)
        if param_dict.get('obj_list'):
            obj_list = param_dict['obj_list']
            obj_num = param_dict['obj_list']['obj_num']
        if param_dict.get('rule_list'):
            rule_list = param_dict['rule_list']

        framesize = height * stride * 3 // 2  # 一帧图像所含的像素个数

        # 第二个参数：可选，默认值为0。给offset参数一个定义，表示要从哪个位置开始偏移；
        # 0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起。
        fp.seek(0, 2)  # 设置文件指针到文件流的尾部
        file_size = fp.tell()  # 当前文件指针位置
        fp.seek(0, 0)

        # order表示行优先 这里先开辟一个yuv的大小
        Yt = np.zeros(shape=(height * 3 // 2, stride), dtype='uint8', order='C')
        for m in range(height * 3 // 2):
            for n in range(stride):
                # 原本是字节串,需要将其转换为整数
                Yt[m, n] = ord(fp.read(1))
        fp.close()

        img = Yt.astype('uint8')
        # 由于 opencv 不能直接读取 YUV 格式的文件, 所以要转换一下格式,大致含义是说将yuv转换为bgr(nv12格式转换)
        bgr_img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_NV12)  # 注意 YUV 的存储格式
        # 画线
        # 动态调整线宽
        if(width*height>2560*1440):
            self.line_width=4
        else:
            self.line_width=2
        self.draw_on_img(width, height, obj_num, obj_list, bgr_img)
        if save_path:
            self.save_img(bgr_img, save_path)
        # # 是否显示图片
        # if disp==False:
        #     return None
        if out_img:
            return bgr_img
        else:
            return None

    def save_img(self, img, path):
        cv2.imwrite(path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        '''
        保存图片.可保存为,jpeg png web
        cv2.CV_IMWRITE_JPEG_QUALITY  设置图片格式为.jpeg或者.jpg的图片质量，其值为0---100（数值越大质量越高），默认95
        cv2.CV_IMWRITE_WEBP_QUALITY  设置图片的格式为.webp格式的图片质量，值为0--100
        cv2.CV_IMWRITE_PNG_COMPRESSION  设置.png格式的压缩比，其值为0--9（数值越大，压缩比越大），默认为3
        '''


class YuvDisper(YuvAnlysiser):
    '''
    yuv 数据显示类,由分析类父类继承而来
    '''

    def __init__(self):
        # 继承父类的私有属性
        super().__init__()
        # 第二个参数输入 0 表示不根据图像打消调整窗口大小
        cv2.namedWindow("YuvDisp", cv2.WINDOW_AUTOSIZE)

    def __del__(self):
        cv2.destroyWindow("YuvDisp")

    def disp_yuv_frame(self, filename, end=None, ):
        img = self.anlysis_yuv_frame(filename, out_img=True, save_path=None)
        cv2.imshow('YuvDisp', img)
        if (type(end) == type('q')):
            # chr()是将数字转化为ascii码,ord则是将ascii码转换为数字
            while (cv2.waitKey(200) != ord(end)):
                pass
        elif (type(end) == type(100)):
            cv2.waitKey(end)
        else:
            # 默认等待1000ms
            cv2.waitKey(1000)

        return None


def main_func():
    disper = YuvDisper()
    file_list = [x for x in os.listdir(yuv_file_path) if '.yuv' in x]
    file_list = list(map(lambda x: os.path.join(yuv_file_path, x), file_list))
    print("find file ", file_list)
    for filename in file_list:
        disper.disp_yuv_frame(filename,end=100)


if __name__ == '__main__':
    main_func()
