# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 07:44:53 2021

@author:  www.51uwb.cn
"""


class global_var:
    _global_anthor = [{'enable': 1, 'short_address': 0x0001, 'x': 0, 'y': 0, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 1, 'short_address': 0x0002, 'x': 1.6, 'y': 0, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 1, 'short_address': 0x0003, 'x': 1.6, 'y': 1.6, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 1, 'short_address': 0x0004, 'x': 0, 'y': 1.6, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 0, 'short_address': 0x0005, 'x': 5, 'y': 5, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 0, 'short_address': 0x0006, 'x': 8, 'y': 6, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 0, 'short_address': 0x0007, 'x': 2, 'y': 8, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 0, 'short_address': 0x0008, 'x': 2, 'y': 9, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 0, 'short_address': 0x0009, 'x': 2, 'y': 9, 'z': 0, 'time': 0, 'qt': 0},
                      {'enable': 0, 'short_address': 0x000A, 'x': 2, 'y': 9, 'z': 0, 'time': 0, 'qt': 0}
                      ]


def set_anthor(value):
    global_var._global_anthor = value


def get_anthor():
    try:
        return global_var._global_anthor
    except KeyError:
        return KeyError
