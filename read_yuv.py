#!/usr/bin/env python
#-*- coding:utf-8 _*-
__author__ = 'LJjia'
# *******************************************************************
#     Filename @    read_yuv.py
#       Author @    Jia LiangJun
#  Create date @    2020/10/14 22:13
#        Email @    LJjiahf@163.com
#  Description @    从yuv数据中读取结构体
# ********************************************************************


import struct
import pprint
import copy
import json

# 结构体头大小
st_head_len=32
# # 结构体数据包大小
# st_data_len=8304
# 单个ojb info结构体大小,对应sizeof(YUV_FRAME_OBJ_INFO) c语言大小
st_obj_info=256

confindence_idx=0
score_idx=1
# 检测出的目标框的id
id_idx=2
# 坐标框第一个数据，相对于obj结构体的的索引
rect_idx=6

# 属性有三个值,label value desc描述字
attr_num_idx=10
attr_list_idx=11
attr_list_size=3
obj_offset=36


def get_attr_desc_idx(list_offset):
    return attr_list_idx + list_offset *attr_list_size + 0

def get_attr_label_idx(list_offset):
    return attr_list_idx + list_offset *attr_list_size + 1

def get_attr_conf_idx(list_offset):
    return attr_list_idx + list_offset *attr_list_size + 2

def sniff_head(handle):
    '''
    嗅探文件头函数
    :param handle:
    :return: >0 认为嗅探成功 负值或0表示嗅探失败
    '''
    if type(handle) == str:
        file = open(handle, 'rb')
    else:
        file = handle
    file.seek(0, 2)
    yuv_file_len = file.tell()
    file.seek(-st_head_len, 2)
    head = file.read(st_head_len)
    st_head = struct.unpack("<8I", head)
    if (2139095298 != st_head[0]):
        # 2139095298对应16进制0x7F800102 刚好是头
        # 由于这个函数仅仅是嗅探,外界可能传入很多不同的图片,因此屏蔽打印
        # print("vaild head ! ret")
        # 如果输入为路径则关闭,为文件句柄则不关闭
        if type(handle) == str:
            file.close()
        return (-1,-1)
    datalen = st_head[1]
    if (datalen > yuv_file_len):
        print("datalen error %s ! filelen %s datalen %s ret" % (datalen, yuv_file_len, st_data_len))
        if type(handle) == str:
            file.close()
        return (-1,-1)
    if type(handle)==str:
        file.close()
    infoFormat=st_head[2]
    return (datalen,infoFormat)

def parse_yuv_info(path):
    if type(path)==str:
        file=open(path,'rb')
    else:
        file=path
    datalen,file_format=sniff_head(file)
    if datalen<=0:
        print("datalen error %s",datalen)
        if type(file) == str:
            file.close()
        return -1
    print("read datalen %s",datalen)
    file.seek(-(datalen+st_head_len),2)
    data=file.read(datalen)
    # loads读取字符串,load读取文件
    param_dict = json.loads(data)
    pprint.pprint(param_dict)
    # 如果输入为路径则关闭,为文件指针则不关闭
    if type(path)==str:
        file.close()

    return param_dict



def run_demo():

    pa_dict=parse_yuv_info("./yuvdata/Datayuv0.yuv")
    print("print result json")
    pprint.pprint(pa_dict)
    # print(pa_dict['obj_list'][0][score_idx],pa_dict['obj_list'][1][score_idx])
    # pprint.pprint(pa_dict)

if __name__ == '__main__':
    run_demo()