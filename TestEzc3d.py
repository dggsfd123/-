# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:05:27 2020

@author: wangyihan
"""


from ezc3d import c3d
path='E:\\机器人\\002.c3d'
c=c3d(path)
print(c['parameters']['POINT'])
point_data = c['data']['points']