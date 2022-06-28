# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:27:12 2021

@author: www.51uwb.cn
"""
import time  # 引入time模块
import re
from Coordinate_process import BP_Process_String #Coordinate_process.py
import sys
import numpy as np


class Trilateration:
    def __init__(self):
        self.position = np.array([[-0.5, -0.5],
                                  [5.5, -0.5],
                                  [5.5, 5.5],
                                  [-0.5, 5.5]])
        self.distances = []
        self.result = 0

    def trilaterate2D(self):
        A = []
        B = []
        # trilateration using SVD
        for idx in range(4):
            if idx == 0:  # i:1 j:4
                x_coefficient = self.position[3][0] - self.position[idx][0]  # x1-xidx
                y_coefficient = self.position[3][1] - self.position[idx][1]  # y1-yidx
                b = 1 / 2 * (self.distances[idx] ** 2 - self.distances[3] ** 2 -
                             ((self.position[idx][0] - self.position[3][0]) ** 2 + (
                                     self.position[idx][1] - self.position[3][1]) ** 2)) \
                    + x_coefficient * self.position[3][0] + y_coefficient * self.position[3][1]
                A.append([x_coefficient, y_coefficient])
                B.append([b])
            else:
                x_coefficient = self.position[0][0] - self.position[idx][0]  # x1-xidx
                y_coefficient = self.position[0][1] - self.position[idx][1]  # y1-yidx
                b = 1 / 2 * (self.distances[idx] ** 2 - self.distances[0] ** 2 -
                             ((self.position[idx][0] - self.position[0][0]) ** 2 + (
                                     self.position[idx][1] - self.position[0][1]) ** 2)) \
                    + x_coefficient * self.position[0][0] + y_coefficient * self.position[0][1]
                A.append([x_coefficient, y_coefficient])
                B.append([b])
        B = np.array(B)
        A_pseudo = np.linalg.pinv(A)
        self.result = np.dot(A_pseudo, B)
        result_x = self.result[0]
        result_y = self.result[1]
        # return x, y position
        return result_x, result_y

    def setDistances(self, distances):
        self.distances = distances

    def setAnthorCoor(self, Anthor_Node_Configure):
        for index in range(len(Anthor_Node_Configure)):
            self.position[index][0] = Anthor_Node_Configure[index][0]
            self.position[index][1] = Anthor_Node_Configure[index][1]


# &&&:80$000A:20$0001:A1B1:11#0002:A2B2:22#0003:A3B3::33#0004:A4B4:44#0005:A5B5:55$CRC####
# 根据约定格式提取数据包里的各个信息
def bphero_dispose(string):
    result_dict = {'tag': 0x1005, 'seq': 7, 'time': 1234, 'anthor_count': 4,'anthor': []}

    # 数据包以&&& 开头
    res = re.findall(r'&&&', string)
    flag = 1
    if len(res) > 0:
        # step1 print message length,ex 76
        temp_string = string.split("$")[0]  # &&&:80$
        data_len = int(temp_string.split(":")[1], 16)

        # tag info
        temp_string = string.split("$")[1]  # 000A:20
        tag_id = int(temp_string.split(":")[0], 16)  # 000A
        tag_seq = int(temp_string.split(":")[1], 16)  # 20
        # print("标签ID: %02X  Seq: %X" % (tag_id, tag_seq))
        result_dict['tag'] = tag_id
        result_dict['seq'] = tag_seq

        # anthor info
        temp_string = string.split("$")[2]  # 0001:A1B1:11#0002:A2B2:22#0003:A3B3:33#0004:A4B4:44#0005:A5B5:55
        anthor_count = len(temp_string.split('#'))
        result_dict['anthor_count'] = anthor_count

        for index in range(anthor_count):
            anthor_info = temp_string.split('#')[index]  # 0001:A1B1:11
            anthor_id = int(anthor_info.split(":")[0], 16)
            anthor_dist = 0.01*int(anthor_info.split(":")[1], 16)   # convert to cm
            print("Anthor%d Distance = %0.2f m"% (index+1, anthor_dist))
            anthor_rssi = int(anthor_info.split(":")[2], 16)
            result_dict['anthor'].append([anthor_id, anthor_dist, anthor_rssi])
        flag = 0
    return flag, result_dict





def Compute_Location(Input_Data):
    Info = BP_Process_String(Input_Data)
    print(Info)
    if Info['count'] < 4:
        result_x = 0
        result_y = 0
        result_flag = 0
    else:
        tril2d = Trilateration()
        tril2d.setDistances(Info['distance'])
        tril2d.setAnthorCoor(Info['anthor'])
        result_x, result_y = tril2d.trilaterate2D()
        result_flag = 1
        print("x = %0.2f, y = %0.2f" % (result_x, result_y))
    return result_flag, Info['seq'], Info['tag'], result_x, result_y


# step1 处理接收来的数据包
def Process_String_Before_Udp(NewString):
    error_flag, result_dic = bphero_dispose(NewString)
    return error_flag, result_dic

def twr_main(input_string):
    print(input_string)
    error_flag, result_dic = Process_String_Before_Udp(input_string)
    if error_flag == 0:
        [location_result, location_seq, location_addr, location_x, location_y] = Compute_Location(result_dic)
        return location_result, location_seq, location_addr, location_x, location_y
    return 0, 0, 0, 0, 0

# test code ==============================
'''
x = 3.2
y = 1
import math
dis1 = math.sqrt((x-0)*(x-0) + (y-0)*(y-0))
print(dis1)
dis2 = math.sqrt((x-10)*(x-10) + (y-0)*(y-0))
print(dis2)
dis3 = math.sqrt((x-10)*(x-10) + (y-10)*(y-10))
print(dis3)
dis4 = math.sqrt((x-0)*(x-0) + (y-10)*(y-10))
print(dis4)

s = '&&&:80$000A:20$0001:%04X:11#0002:%04X:22#0003:%04X:33#0004:%04X:44$CRC####' % (int(dis1*100), int(dis2*100),int(dis3*100),int(dis4*100))
print(s)
twr_main(s)
'''
# test code end ===========================

