#!/usr/bin/env python
#-*- coding:utf-8 _*-
__author__ = 'LJjia'
# *******************************************************************
#     Filename @    GetXYPos.py
#       Author @    Jia LiangJun
#  Create date @    2020/5/10 15:29
#        Email @    LJjiahf@163.com
#  Description @    根据读取的内容获取XY表达式,其间需要利用正则表达式处理
# ********************************************************************


import re

def convert_normalized(x1,y1,width,height):
    '''
    将像素值形式的xy坐标转化为归一化坐标
    :param x1:
    :param y1:
    :param width: 原图像宽高
    :param height:
    :return: 归一化之后小数形式的[x1,y1]
    '''
    return [x1/width,y1/height]

def parse_position(input_str,re_expression):
    '''
    通过正则表达式解析字符串,输入的x,y坐标都x1,y1的形式传入,相当于传入占位符,解析的时候将其解析为数字,每次送入一行的数据
    :param input_str:带解析的字符串
    :param re_expression:输入的正则表达式字符串 以字符$代表float类型数字
    :return: 坐标xy的list 形式如[[x1,y1],[x2,y2]...]
    '''
    # 替换 *和$
    expression=re_expression.replace('*', r'.*?')
    expression = expression.replace("$", r"(\d+\.\d+)")
    parse_result=re.findall(expression,input_str)
    # 得到的结果是一个列表中的元组,剥掉列表壳,返回元组
    if parse_result and parse_result[0]:
        tuple_result=tuple(map(float,parse_result[0]))
        return tuple_result
    else:
        return None

def parse_file(input_str,re_expression):
    '''
    读取一整个的日志信息,转换成归一化的float返回,类似于对parse_position函数的封装
    :param input_str:长串的字符串内容,可能有多行
    :param re_expression:正则表达式
    :return:
    '''
    input_line_list=input_str.split('\n')
    result=[]
    for line in input_line_list:
        # print("input log every line value ",line)
        tmp=parse_position(line,re_expression)
        if(tmp):
            # 排除None类型
            result.append(tmp)
    # print("解析结果",result)
    return result



def demo_test(input_data,re_ex):
    '''
    demo 测试函数
    :param input_data:
    :param re_ex:
    :return:
    '''
    print("input data %s re_ex %s"%(input_data,re_ex))
    reslut=parse_file(input_data,re_ex)
    print(reslut)





if __name__ == '__main__':
    demo_input_str = "chan 5 x y float : 0.4 0.8 1.000 0.85656 0.75151 0.7455\n : 0.4 0.5 1.000 0.85656 0.75151 0.7455"
    demo_re_ex = "*: $ $ $ $"
    demo_test(demo_input_str,demo_re_ex)