from scipy.interpolate import interp1d
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import time
import bcapclient
import csv

###変数
x=[1,2,3,4,5,6,7,8,9,10]
y=[]
###RC8のIPアドレス、ポート番号（固定値）、Timeoutの設定
host = "192.168.0.1"
port = 5007
timeout = 2000



###補間用関数
def get_interpolate_data(x, y, num, kind):
    f_CS = interp1d(x, y, kind=kind)
    #x_new = np.linspace(np.min(x), np.max(x), num=num)
    x_new = np.linspace(0, np.pi, num=num)[::-1]
    x_new = np.min(x) + (1 + np.cos(x_new)) * (np.max(x) - np.min(x)) /2
    y_new = f_CS(x_new)
    return np.round(x_new,2), np.round(y_new,2)

def get_move_pos(x,y,J_num,num):
    x[J_num-1]=str(y[num])
    return x


###入力データ
csvfile = 'J1_to_J6.csv'
f = open(csvfile,"r")
reader = csv.reader(f)
'CSVからデータ取得し格納'
for column in reader:
    y.append(column[0])
f.close()
'数値データに変換'
y = list(map(float,y))
'始点から終点まで何点で表すか'
num =500 
'3次スプライン補間'
kind = "cubic"
'関数実行'
x_new, y_new = get_interpolate_data(x, y, num, kind)



###接続処理 TCP
m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
print("Open Connection")

###b_cap通信開始
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

###パラメーターの設定
Name = ""
Provider="CaoProv.DENSO.VRC"
Machine = ("localhost")
Option = ("")

###RC8プロバイダと接続
hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
print("Connect RC8")
###Robot Object Handl取得
HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
print("AddRobot")

###TakeArm
Command = "TakeArm"
Param = [0,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("TakeArm")

###Motor On
Command = "Motor"
Param = [1,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("Motor On")

###ExtSpeed,Accel,Decel設定
Command = "ExtSpeed"
Speed = 30
Accel = 10
Decel = 10
Param = [Speed,Accel,Decel]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("ExtSpeed")


###動作初期位置に移動（slave modeに移行するために初期値をそろえるため）
Comp=1
Pos_value = [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0]
Pose = [Pos_value,"J","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E J(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)")
time.sleep(1)

###Slave move: Change return format
Command = "slvRecvFormat"
# Param = 0x0001  # Change the format to position
#Param = 0x0014  # hex(10): timestamp, hex(1): [pose, joint]
Param = 0x0002  # hex(10): timestamp, hex(1): [pose, joint]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

###Slave move: Change mode
Command = "slvChangeMode"
#Param = 0x101  # Type P, mode 1 (overwrite the destination)  
# Param = 0x001  # Type P, mode 0 (buffer the destination)  
#Param = 0x002  # Type J, mode 0 (overwrite the joint)
Param = 0x102  # Type J, mode 1 (buffer the joint)  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))


###Send POS slvMove
Command = "slvMove"
LoopNum = num-1
Pos_value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
J_num = 1
cnt1 = 0.005
cnt2 = 0.007
for num in range(LoopNum):
    x = get_move_pos(Pos_value,y_new,J_num,num)
    print(Pos_value)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print(time : ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt1)
for num in range(LoopNum):
    Pos_value =  get_move_pos(Pos_value,y_new,J_num,LoopNum-num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt1)

J_num = 2
for num in range(LoopNum):
    Pos_value = get_move_pos(Pos_value,y_new,J_num,num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt2)
for num in range(LoopNum):
    Pos_value =  get_move_pos(Pos_value,y_new,J_num,LoopNum-num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt2)

J_num = 3
for num in range(LoopNum):
    Pos_value = get_move_pos(Pos_value,y_new,J_num,num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt2)


J_num = 4
for num in range(LoopNum):
    Pos_value = get_move_pos(Pos_value,y_new,J_num,num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt1)
for num in range(LoopNum):
    Pos_value =  get_move_pos(Pos_value,y_new,J_num,LoopNum-num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt1)

J_num = 5
for num in range(LoopNum):
    Pos_value = get_move_pos(Pos_value,y_new,J_num,num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt2)


J_num = 6
for num in range(LoopNum):
    Pos_value = get_move_pos(Pos_value,y_new,J_num,num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt1)
for num in range(LoopNum):
    Pos_value =  get_move_pos(Pos_value,y_new,J_num,LoopNum-num)
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    print(ret)
    #print("time:" + str(ret[0]))
    #print("pos P,J:" + str(ret[1]))
    time.sleep(cnt1)


###Slave move: Change mode
Command = "slvChangeMode"  
Param = 0x000  # finish Slave Move  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))
time.sleep(3)

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

###Handle解放
if HRobot != 0:
    m_bcapclient.robot_release(HRobot)
    print("Release Robot")
if hCtrl != 0:
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")


###b-cap通信終了
m_bcapclient.service_stop()
print("b-cap service Stop")

del m_bcapclient
print("Finish")
