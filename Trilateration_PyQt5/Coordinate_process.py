# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:19:00 2021

@author:  www.51uwb.cn

"""


# 定义一个三维坐标的类
class Vector3:
    def __init__(self):
        self.x = 0  #
        self.y = 0  #
        self.z = 0  #


import globalvar
import time  # 引入time模块


# 根据基站的地址，在基站配置列表中获取基站的三维坐标
def Find_Anthor_Coor(Athor_Addr):
    gAnthor_Node_Configure = globalvar.get_anthor()
    for item in gAnthor_Node_Configure:
        if item['short_address'] == int(Athor_Addr) and item['enable'] == 1:
            item['time'] = time.time()
            return [1, item['x'], item['y'], item['z']]
    return [0, 0, 0, 0]


# 处理基站相关信息，获取基站的坐标和对应的时钟timestamp
# 传入的list 类型[['0003', 230800053236.2253, 10], ['0002', 230800053046.89203, 10], ['0001', 230800053463.46512, 10], ['0004', 230800053532.30975, 10]]
# list 中三项，基站地址，已经同步后的timestamp 以及信号强度
def Anthor_Coordinate_Process(Anthor_info):
    Coorinate_List = []
    TimeStamp_List = []
    RSSI_List = []
    Find_Anthor_Flag = 0
    # loop anthor list
    for item in Anthor_info:
        Anthor_Address = item[0]  # 获取基短地址
        [flag, x, y, z] = Find_Anthor_Coor(Anthor_Address)  # 从配置信息中获取该基站对应的三维坐标
        if flag == 1:  # 基站配置信息获取到基站的三维坐标
            Coorinate_List.append([x, y, z])  # 将三维坐标追加的List中
            TimeStamp = item[1]  # 提取时间戳信息，只提取那些基站地址匹配到的时间信息，与基站一一对应
            TimeStamp_List.append(TimeStamp)  # 将时间戳信息追加到List中
            Rssi = item[2]
            RSSI_List.append(Rssi)
            Find_Anthor_Flag = 1  # 标记找到基站
    return Find_Anthor_Flag, Coorinate_List, TimeStamp_List, RSSI_List


# input
# {'tag': 10, 'seq': 32, 'time': 1234, 'anthor_count': 5, 'anthor': [[1, 41393, 17], [2, 41650, 34], [3, 41907, 51], [4, 42164, 68], [5, 42421, 85]]}
# output
# {'tag': 10, 'seq': 32, 'count': 5, 'anthor': [[0, 0, 0], [10, 0, 0], [10, 10, 0], [0, 10, 0], [5, 5, 0]], 'distance': [41393, 41650, 41907, 42164, 42421], 'Rssi': [17, 34, 51, 68, 85]}
def BP_Process_String(Input_String):
    #    print(Input_String)

    Anthor_Address = Vector3()

    # 返回数据
    # {'tag': '0008', 'seq': 186, 'anthor':[[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]],'distance': [120,45,9]}
    New_Dict = {'tag': 0, 'seq': 0, 'count': 0, 'anthor': [], 'distance': [], 'Rssi': []}
    New_Dict['tag'] = Input_String['tag']
    New_Dict['seq'] = Input_String['seq']

    # 提出基站信息
    (Anthor_Flag, Coor_Address, Dist_Stamp, Rssi_List) = Anthor_Coordinate_Process(Input_String['anthor'])
    if Anthor_Flag == 0:
        print("Error! Could Not Find ANTHOR Node Address !!")
        return New_Dict
    for index in range(len(Coor_Address)):
        Anthor_Address.x = Coor_Address[index][0]
        Anthor_Address.y = Coor_Address[index][1]
        Anthor_Address.z = Coor_Address[index][2]
        New_Dict["anthor"].append([Anthor_Address.x, Anthor_Address.y, Anthor_Address.z])
        New_Dict["distance"].append(Dist_Stamp[index])
        New_Dict["Rssi"].append(Rssi_List[index])
    # 记录有多少个基站在配置文件找到对应坐标信息
    New_Dict["count"] = len(Coor_Address)
    return New_Dict

# print(BP_Process_String({'tag': 10, 'seq': 32, 'time': 1234, 'anthor_count': 5, 'anthor': [[1, 41393, 17], [2, 41650, 34], [3, 41907, 51], [4, 42164, 68], [5, 42421, 85]]}) )
