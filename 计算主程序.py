# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 17:05:40 2021

@author: 001
"""
import numpy as np
from math import sin,cos,tan,acos,atan
import cv2

import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

pi = 3.1415926


def modlen(a,b):
    x1,y1,z1 = a
    x2,y2,z2 = b
    l = np.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    return format(l,'.1f')

#计算角度，可二维和三维
def findangle(x,y):
    l_x = np.sqrt(x.dot(x))
    l_y = np.sqrt(y.dot(y))
    dian = x.dot(y)
    cos_= dian / (l_x * l_y)
    angle_r = np.arccos(cos_)
    angle_d = angle_r * 180 / np.pi
    return float(format(angle_d,'.1f'))

def bonelen(sp1,sp3,neck,uparm,lowarm,hand):
    newpoint = np.array([(sp3[0] + neck[0])//2,(sp3[1] + neck[1])//2,(sp3[2] + neck[2])//2])
    l1 = modlen(newpoint,sp1)
    l2 = modlen(newpoint,uparm)
    l3 = modlen(uparm,lowarm)
    l4 = modlen(lowarm,hand)
    return l1,l2,l3,l4

def model():
# =============================================================================
#                neck
#                 |
#                 |    l2 = 22.3        
#              newpoint---------uparm
#                 |               |
#                 |               |   l3 = 29.4
#               spine3            |
#    l1 = 32.0    |             lowarm
#                 |               |
#                 |               |   l4 = 24.0
#               spine1            |
#                 |             hand
#               pevis22
#                 ^
#                 |y
#                 ---->z
# =============================================================================
    return

def caltheta(sp1,sp3,neck,uparm,lowarm,hand):
    newpoint = np.array([(sp3[0] + 4*neck[0])//5,(sp3[1] + 4*neck[1])//5,(sp3[2] + 4*neck[2])//5])

    #print(sp1,sp3,neck,newpoint,uparm,lowarm,hand)

    vector_jian = np.array([uparm[0]-newpoint[0],uparm[1]-newpoint[1],uparm[2]-newpoint[2]]) 
    yao_angle = findangle(vector_jian,np.array([0,0,1]))
    
    vector_dabi = np.array([lowarm[0]-uparm[0],lowarm[1]-uparm[1],lowarm[2]-uparm[2]])

    naxis = np.cross(vector_jian,np.array([0,1,0]))
    flla,fllb,fllc = findangle(vector_dabi,naxis),findangle(vector_dabi,np.array([0,1,0])),findangle(vector_dabi,vector_jian)
    dabizhang_angle = int(180-fllb)
    dabiqianhou_angle = -int(90-flla)


    # R_jian = cv2.Rodrigues(vector_jian)
    # vector_dabirotate = np.dot(R_jian[0],vector_dabi)
    # dabiqianhou_angle = int(atan(vector_dabirotate[0]/vector_dabirotate[1])*180)
    # dabizhang_angle = int(atan(vector_dabirotate[2]/vector_dabirotate[1])*180)

    #dabiqianhou_angle = int(findangle(np.array([vector_dabi[0],vector_dabi[1],vector_dabi[2]]),np.array([0,-1,0])))
    #dabizhang_angle = int(findangle(np.array([vector_dabi[0],vector_dabi[1],vector_dabi[2]]),np.array([vector_jian[0],vector_jian[1],vector_jian[2]])))
    #zongzhuan = findangle(vector_dabi,vector_jian)

    
    vector_xiaobi = np.array([hand[0]-lowarm[0],hand[1]-lowarm[1],hand[2]-lowarm[2]])
    zhou_angle = int(findangle(vector_xiaobi,vector_dabi))
    
    #return yao_angle,dabiqianhou_angle,dabizhang_angle,zhou_angle
    return dabiqianhou_angle, dabizhang_angle, zhou_angle


def readcsv(path):
    f = csv.reader(open(path,'r'))
    data = []
    for _ in f:
        data.append(_)
    return data

def dealdata(data):
    dealdata = []
    m = len(data)
    for i in range(7,m,12):
        dealdata.append(data[i])
    return dealdata

def data2bones(dealdata):
    m = len(dealdata)
    sp1,sp3,neck,uparm,lowarm,hand = [],[],[],[],[],[]
    for i in range(m):
        sp1x = (float(dealdata[i][13]))
        sp1y = (float(dealdata[i][14]))
        sp1z = (float(dealdata[i][15]))
        sp1.append([float(format(sp1x,'.2f')),float(format(sp1y,'.2f')),float(format(sp1z,'.2f'))])
        
        sp3x = float(dealdata[i][20])
        sp3y = float(dealdata[i][21])
        sp3z = float(dealdata[i][22])
        sp3.append([float(format(sp3x,'.2f')),float(format(sp3y,'.2f')),float(format(sp3z,'.2f'))])
                
        neckx = float(dealdata[i][27])
        necky = float(dealdata[i][28])
        neckz = float(dealdata[i][29])
        neck.append([float(format(neckx,'.2f')),float(format(necky,'.2f')),float(format(neckz,'.2f'))])
        
        uparmx = float(dealdata[i][48])
        uparmy = float(dealdata[i][49])
        uparmz = float(dealdata[i][50])
        uparm.append([float(format(uparmx,'.2f')),float(format(uparmy,'.2f')),float(format(uparmz,'.2f'))])
        
        lowarmx = float(dealdata[i][55])
        lowarmy = float(dealdata[i][56])
        lowarmz = float(dealdata[i][57])
        lowarm.append([float(format(lowarmx,'.2f')),float(format(lowarmy,'.2f')),float(format(lowarmz,'.2f'))])
        
        handx = float(dealdata[i][62])
        handy = float(dealdata[i][63])
        handz = float(dealdata[i][64])
        hand.append([float(format(handx,'.2f')),float(format(handy,'.2f')),float(format(handz,'.2f'))])
    
    return sp1,sp3,neck,uparm,lowarm,hand

def draw(p1,p2,p3,p4,p5,p6):
    x = [p1[0],p2[0],p3[0],p4[0],p5[0],p6[0]]
    z = [p1[1],p2[1],p3[1],p4[1],p5[1],p6[1]]
    y = [p1[2],p2[2],p3[2],p4[2],p5[2],p6[2]]
    #print(x,y,z)
    
    fig = plt.figure()
    ax = Axes3D(fig)
    auto_add_to_figure=False
    fig.add_axes(ax)
    ax.scatter(x, y, z, color=[0,0,0,1], s=100)
    ax.view_init(elev=0, azim=0)
    ax.legend(loc='best')
    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'black'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'black'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'black'})
    plt.show()

def writetxt(x,txtpath):
    with open(txtpath,"a") as f:
        f.write(str(x))

path = r'E:\\机器人\\03.csv'
initdata = readcsv(path)
points = dealdata(initdata)

spine1,spine3,neck,uparm,lowarm,hand = data2bones(points)




txtpath = 'E:\\机器人\\rawpoint.txt'
#writetxt(spine1,txtpath)
#print(caltheta(spine1[t],spine3[t],neck[t],uparm[t],lowarm[t],hand[t]))
for i in range(1,len(spine1)):
    aa,bb,cc = caltheta(spine1[i],spine3[i],neck[i],uparm[i],lowarm[i],hand[i])
    writetxt("["+format((aa*pi/180),'.4f')+" "+format((bb*pi/180),'.4f')+" "+format((cc*pi/180),'.4f')+" 0 0 0]"+"\n",txtpath)




print("lenth")
print(bonelen(spine1[0],spine3[0],neck[0],uparm[0],lowarm[0],hand[0]))


theta = []
for i in range(len(spine1)):
    theta.append(caltheta(spine1[i],spine3[i],neck[i],uparm[i],lowarm[i],hand[i]))
print("theta")
print(theta)

t = 50
draw(spine1[t],spine3[t],neck[t],uparm[t],lowarm[t],hand[t])

# fig = plt.figure()
# ims = []
# for t in range(1,131,5):
#     im = draw(spine1[t],spine3[t],neck[t],uparm[t],lowarm[t],hand[t])
#     ims.append(im)
# ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=1000)
# ani.save("test.gif",writer='pillow')

#for t in range(140):
#    draw(spine1[t],spine3[t],neck[t],uparm[t],lowarm[t],hand[t])
#print(theta)




