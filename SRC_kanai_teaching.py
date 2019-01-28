# -*- coding:utf-8 -*-
#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

#import pybcapclient.bcapclient as bcapclient
import bcapclient
import time
from scipy.interpolate import interp1d
import numpy as np
#import matplotlib.pyplot as plt
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
Delay_300=[6,12,19,22,34,42,46,56,61,67,70,73,81,84,92,126,140,171,175,177,187]
Delay_400=[158,160,162]
Delay_500=[29,59,101,103,105,121,128,133,182,193,198]
Delay_600=[75]
Delay_1000=[2,31,87,89,136,142,148,156,164,166,189,194]
Delay_2000=[78,95,119,120,154,167]
Pos_Value=[0.0 , 0.0 , 90.0 , 0.0 , 90.0 , 0.0]

###RC8 or VRC
#control_mode = "RC8"
control_mode = "VRC"


###座標格納関数
def get_move_pos(J_pos,J1,J2,J3,J4,J5,J6,P):
    J_pos[0]=J1[P-1]
    J_pos[1]=J2[P-1]
    J_pos[2]=J3[P-1]
    J_pos[3]=J4[P-1]
    J_pos[4]=J5[P-1]
    J_pos[5]=J6[P-1]
    return J_pos



###ロボット制御用関数(Comp1:Move P,2:Move L,3:Move C,4:Move S)
def robot_cont(Command,Speed,Accel,Decel,Comp,Pos_value,Mode1,Mode2):
    ### set ExtSpeed,Accel,Decel
    if Command==1:
        Command = "ExtSpeed"
    Param = [Speed,Accel,Decel]
    m_bcapclient.robot_execute(HRobot,Command,Param)
    print("ExtSpeed")
    
    ###Select Mode
    if Mode1==1:
        Mode1 = "J"
    elif Mode1 == 2:
        Mode1 = "P"
    if Mode2==1:
        Mode2 = "@P"
    elif Mode2 == 2:
        Mode2 = "@E"

    ### Move Position
    Pose = [Pos_value,Mode1,Mode2]
    m_bcapclient.robot_move(HRobot,Comp,Pose,"")
    print("Complete Move:",Pos_value,i)

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


#--------------------------------前処理--------------------------------#

### set IP Address , Port number and Timeout of connected RC8 or VRC
if control_mode == "RC8":
    host = "192.168.0.1"
elif control_mode == "VRC":
    host = "192.168.0.20"
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

Comp=1
Pos_value = [0.0 , 0.0 , 90.0 , 0.0 , 90.0 , 0.0]
Pose = [Pos_value,"J","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")
time.sleep(1)

#--------------------------------ロボット動作命令部--------------------------------#
for i in range(1,202):
    ###座標の設定は引数8番目の変える（P8なら8にする、SRC_組立動作(J型)フローのNo8に対応
    Pos_value = get_move_pos(Pos_value,J1,J2,J3,J4,J5,J6,i)

    if i == 202:
        robot_cont(1,10,25,25,1,Pos_value,1,2)
    else:
        robot_cont(1,10,25,25,2,Pos_value,1,1)
    #time.sleep(0.5)
    if i in Delay_300:
        delay=0.3
    elif i in Delay_400:
        delay=0.4 
    elif i in Delay_500:
        delay=0.5 
    elif i in Delay_600:
        delay=0.6 
    elif i in Delay_1000:
        delay=1 
    elif i in Delay_2000:
        delay=2 
    else:
        delay=0
    time.sleep(delay)


#--------------------------------後処理--------------------------------#
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



"""サンプル
### set ExtSpeed,Accel,Decel
Command = "ExtSpeed"
Speed = 20
Accel = 25
Decel = 25
Param = [Speed,Accel,Decel]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("ExtSpeed")

### Move Initialize Position
Comp=1
Pos_value = [0.0 , 0.0 , 90.0 , 0.0 , 90.0 , 0.0]
Pose = [Pos_value,"J","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")
"""