# -*- coding:utf-8 -*-

# Sample program
# b-cap slave mode 

#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

#import pybcapclient.bcapclient as bcapclient
#import bcapclient
import time
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import csv

###変数
x=[]
J1=[]
J2=[]
J3=[]
J4=[]
J5=[]
J6=[]
Pos_value=[0,0,0,0,0,0]

###座標格納関数
def get_move_pos(J_pos,J1,J2,J3,J4,J5,J6,Position):
    J_pos[0]=J1[Loopnum]
    J_pos[1]=J2[Loopnum]
    J_pos[2]=J3[Loopnum]
    J_pos[3]=J4[Loopnum]
    J_pos[4]=J5[Loopnum]
    J_pos[5]=J6[Loopnum]
    return J_pos

###入力データ
csvfile = 'SRC_J.csv'
f = open(csvfile,"r")
reader = csv.reader(f)
'CSVからデータ取得し格納'
count = 0
for column in reader:
    J1.append(column[0])
    J2.append(column[1])
    J3.append(column[2])
    J4.append(column[3])
    J5.append(column[4])
    J6.append(column[5])
    x.append(count)
    count+=1
f.close()

'リストをfloatに変換'
J1=list(map(float, J1))
J2=list(map(float, J2))
J3=list(map(float, J3))
J4=list(map(float, J4))
J5=list(map(float, J5))
J6=list(map(float, J6))

###座標の設定は引数8番目の変える（P8なら8にする）
Pos_value = get_move_pos(Pos_value,J1,J2,J3,J4,J5,J6,1)


### set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000

### Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
print("Open Connection")

### start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

### set Parameter
Name = ""
Provider="CaoProv.DENSO.VRC"
Machine = ("localhost")
Option = ("")

### Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
print("Connect RC8")
### get Robot Object Handl
HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
print("AddRobot")

### TakeArm
Command = "TakeArm"
Param = [0,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("TakeArm")

### Motor On
Command = "Motor"
Param = [1,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("Motor On")

### Move Initialize Position
Comp=1
Pos_value = [0.0 , 0.0 , 90.0 , 0.0 , 90.0 , 0.0]
Pose = [Pos_value,"J","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")
time.sleep(1)

### set ExtSpeed,Accel,Decel
Command = "ExtSpeed"
Speed = 20
Accel = 25
Decel = 25
Param = [Speed,Accel,Decel]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("ExtSpeed")

###Motor Off
Command = "Motor"
Param = [0,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("Motor Off")

###Give Arm
Command = "GiveArm"
Param = None
m_bcapclient.robot_execute(HRobot,Command,Param)
print("GiveArm")



### Release Handle and Disconnect
if HRobot != 0:
    m_bcapclient.robot_release(HRobot)
    print("Release Robot")
if hCtrl != 0:
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")



### b-cap service stop
m_bcapclient.service_stop()
print("b-cap service Stop")

del m_bcapclient
print("Finish")
