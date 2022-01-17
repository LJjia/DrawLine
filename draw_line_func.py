#!/usr/bin/env python
# -*- coding:utf-8 _*-
__author__ = 'LJjia'
# *******************************************************************
#     Filename @    draw_line_func.py
#       Author @    Jia LiangJun
#  Create date @    2020/5/13 22:24
#        Email @    LJjiahf@163.com
#  Description @    画线功能
# ********************************************************************


from PIL import Image, ImageDraw
import shutil

#  文件路径先写死
output_img_dir = './image/draw_line_tmp'
image_type = 'jpg'
output_img_path = output_img_dir + '.' + image_type

if (image_type == 'jpg'):
    img_save_mode = 'JPEG'
elif (image_type == 'png'):
    img_save_mode = 'PNG'


# bmp 形式不考虑

def parse_file_suffix(path):
    '''
    解析文件后缀,并返回小写字母的文件类型 'jpg' 'png' 'bmp'
    :param path:
    :return:
    '''
    file_suffix=path.split('.')[-1]
    file_suffix=file_suffix.lower()
    if file_suffix=='jpg' or file_suffix=='jpeg':
        return 'jpg'
    elif file_suffix=='png':
        return 'png'
    elif file_suffix=='bmp':
        return 'bmp'
    else:
        return None

def convert_file_type_to_jpeg(file_path,save_path):
    '''
    将图片转换成jpeg格式并且保存到相应的路径,相当于滤除不支持的格式
    :param file_path:
    :param save_path:
    :return:
    '''
    img_format=parse_file_suffix(file_path)
    if not img_format:
        print("file type path(%s) not support"%file_path)
        return None
    elif img_format=='jpg':
        shutil.copy(file_path,save_path)
        return True
    print(img_format,file_path,save_path)
    img=Image.open(file_path)
    img.save(save_path,"JPEG")
    print(img_format, file_path,save_path)
    return True

def get_pic_param(file_path):
    img = Image.open(file_path)
    return img.size

def float_to_pixel(img_width, img_heigth, float_x, float_y):
    '''
    归一化坐标转化为像素坐标
    :param img_width:
    :param img_heigth:
    :param float_x:
    :param float_y:
    :return:
    '''
    if float_x > 1 and float_y > 1:
        print("date error")
        return (int(float_x), int(float_y))
    return (int(img_width * float_x), int(img_heigth * float_y))


def draw_point(image_path, pos_list, color, pixel_size):
    '''
    画点函数
    :param image_path:图片路径
    :param pos_list:点列表
    :param color:点颜色
    :param pixel:点占几个像素
    :return:
    '''
    img = Image.open(image_path)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    for point in pos_list:
        if (type(point[0]) == float or type(point[1]) == float):
            point = float_to_pixel(w, h, point[0], point[1])
        if (pixel_size == 1):
            draw.point(point, fill=color)
        elif (pixel_size > 1):
            draw.rectangle([point, (point[0] + pixel_size, point[1] + pixel_size)], fill=color)
        else:
            return
    img.save(output_img_path, img_save_mode)


def float_to_pixel_list(img_width, img_heigth, point_list):
    '''
    归一化坐标转像素坐标,输入输出都是list类型,自动判断
    :param img_width:
    :param img_heigth:
    :param point_list:
    :return:
    '''
    if not point_list:
        if (point_list[0][0] > 1 and point_list[0][1] > 1):
            print("not float type")
            return point_list
    result_list = []
    for point in point_list:
        if (len(point) == 2):
            result_list.append((int(point[0] * img_width), int(point[1] * img_heigth)))
        elif (len(point) == 4):
            # 如果是[(x,y,w,h)]这种类型
            result_list.append(
                (int(point[0] * img_width), int(point[1] * img_heigth), int(point[2] * img_width), int(point[3] * img_heigth)))
    return result_list


def draw_line(image_path, pos_list, color, pixel_size):
    '''
    画线函数 pos_list中每个元素为点坐标,不用转化,直接可以画线
    :param image_path:
    :param pos_list:
    :param color:
    :param pixel_size:
    :return:
    '''
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    if (pos_list[0][0] <= 1 and pos_list[0][1] <= 1):
        pos_list = float_to_pixel_list(w, h, pos_list)

    draw.line(pos_list, fill=color, width=pixel_size)
    if (len(pos_list) >= 2):
        draw.line([pos_list[0], pos_list[-1]], fill=color, width=pixel_size)
    img.save(output_img_path, img_save_mode)


def draw_rectangle(image_path, pos_list, color, pixel_size):
    '''
    画矩形
    :param image_path:
    :param pos_list:矩形左上角定点坐标和 宽高 wh 传入参数如[(0.1,0.1,0.3,0.4),(0.2,0.2,0.5,0.4)]
    :param color:
    :param pixel_size:矩形线宽
    :return:
    '''
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # 如果xy坐标为归一化坐标
    if (pos_list[0][0] <= 1 and pos_list[0][1] <= 1):
        pos_list = float_to_pixel_list(w, h, pos_list)
    print(pos_list)
    for rect in pos_list:
        # 原来的类型是(x,y,w,h)需要转化一下  变成(x1,y1,x2,y2)
        rect_wh=(rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3])
        draw.rectangle(rect_wh, fill=None, outline=color, width=pixel_size)
    img.save(output_img_path, img_save_mode)


def test_demo():
    image_path = './test/test_img.jpg'
    pos_list = [(0.1, 0.1), (0.5, 0.1), (0.5, 0.5), (0.1, 0.5)]
    retangle_list = [(0.1, 0.1, 0.1, 0.1), (0.3, 0.3, 0.1, 0.5)]
    color = 'red'
    pixel_size = 4
    # draw_line(image_path,pos_list,color,pixel_size)
    # img_line=Image.open(output_img_path)
    # img_line.show()
    # draw_point(image_path, pos_list, color, pixel_size)
    # img_point = Image.open(output_img_path)
    # img_point.show()

    draw_rectangle(image_path, retangle_list, color, pixel_size)
    img_rectangle = Image.open(output_img_path)
    img_rectangle.show()


if __name__ == '__main__':
    test_demo()
