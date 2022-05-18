#!/usr/bin/env python
# coding=utf-8
'''
Author: liangjun.jia
Date : Do not edit
LastEditors: liangjun.jia
LastEditTime: 2022-04-25 19:35:20
Description: 关于点和转换的相关函数

Copyright (c) 2022 by Moore Threads, All Rights Reserved. 
'''



from enum import Enum,unique
import re

@unique
class POINT_FORMAT(Enum):
    '''
    description: 点集种类枚举
    param {*}
    return {*}
    '''    
    # 点坐标
    XY=0,
    # 矩形坐标
    XYWH=1, #左上角xy+整体宽高
    CXYWH=2, # 中心xy坐标+整体宽高
    X1X2Y1Y2=5,
    X1Y1X2Y2=6,
    # 点集坐标
    XY_LIST=10,

class POINT_VALUE(Enum):
    '''
    description: 点是归一化还是绝对值枚举
    param {*}
    return {*}
    '''    
    NORMAL=0,
    ABSOLUTE=1,


'''
description: 由src_format转换到xywh格式
param {*} point
param {*} src_format
return {*}
'''
def trans_rect_point_to_xywh(point,src_format):
    if len(point)!=4:
        print("func point_format_trans param error %s"%point)
    if src_format==POINT_FORMAT.XYWH:
        return point
    elif src_format==POINT_FORMAT.CXYWH:
        return (point[0]-point[2]/2,point[1]-point[3]/2,point[2],point[3])
    elif src_format==POINT_FORMAT.X1X2Y1Y2:
        return (point[0],point[2],point[1]-point[0],point[3]-point[2])
    elif src_format==POINT_FORMAT.X1Y1X2Y2:
        return (point[0],point[1],point[2]-point[0],point[3]-point[1])


'''
description: 从xywh格式转换到dst_format格式
param {*} point
param {*} dst_format
return {*}
'''
def trans_rect_point_from_xywh(point,dst_format):
    if len(point)!=4:
        print("func point_format_trans param error %s"%point)
    if dst_format==POINT_FORMAT.XYWH:
        return point
    elif dst_format==POINT_FORMAT.CXYWH:
        return (point[0]+point[2]/2,point[1]+point[3]/2,point[2],point[3])
    elif dst_format==POINT_FORMAT.X1X2Y1Y2:
        return (point[0],point[0]+point[2],point[1],point[1]+point[3])
    elif dst_format==POINT_FORMAT.X1Y1X2Y2:
        return (point[0],point[1],point[2]+point[0],point[3]+point[1])

def rect_point_format_trans(point,src_format,dst_format):
    '''
    description: 点集格式转换
    param {*}
    return {*}
    '''
    # param check
    if len(point)!=4:
        print("func point_format_trans param error %s"%point)
    if src_format in POINT_FORMAT and dst_format in POINT_FORMAT:
        # 转换成中间表达,再转换成输出
        tmp=trans_rect_point_to_xywh(point,src_format)
        ret=trans_rect_point_from_xywh(tmp,dst_format)
        return ret
    else :
        print("input type %s to %s not implement!!"%(src_format,dst_format))
        return (0,0,0,0)
        # raise ValueError("input type %s to %s"%(src_format,dst_format))


def rec_point_value():
    '''
    description: 识别点集是归一化还是绝对值
    param {*}
    return {*}
    '''    
    pass

def abs_convert_normal(point,width,height):
    '''
    将像素值形式的xy坐标转化为归一化坐标
    :param x1:
    :param y1:
    :param width: 原图像宽高
    :param height:
    :return: 归一化之后小数形式的[x1,y1]
    '''
    # 长度必须是2的倍数
    if not len(point)%2==0:
        print("point",point,'len error',len(point))
        return []
    if len(point)==2:
        # 证明是点
        return [point[0]/width,point[1]/height]    
    elif len(point)==4:
        # 证明是矩形
        return [point[0]/width,point[1]/height,point[2]/width,point[3]/height]
    else:
        # 如果是点集,比如 4 6 8这种长度
        ret=[]
        for idx,item in enumerate(point):
            if idx%2==0:
                ret.append(item/width)
            else:
                ret.append(item/height)
        return ret
