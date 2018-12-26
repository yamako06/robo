# -*- coding:utf-8 -*-

# Sample program
# b-cap slave mode 

#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

#import pybcapclient.bcapclient as bcapclient
import bcapclient
import time
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

###Set Parameters
Comp=1
Pos_value = [300.5,-452.0,366.4,179.5,-0.8,175.7,-1]
Pose = [Pos_value,"P","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
time.sleep(1)

### Slave move: Change return format
Command = "slvRecvFormat"
# Param = 0x0001  # Change the format to position
Param = 0x0014  # hex(10): timestamp, hex(1): [pose, joint]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

### Slave move: Change mode
Command = "slvChangeMode"
Param = 0x101  # Type P, mode 1 (overwrite the destination)  
# Param = 0x001  # Type P, mode 0 (buffer the destination)  
# Param = 0x102  # Type J, mode 1 (overwrite the joint)  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))


### Send POS slvMove
Command = "slvMove"
LoopNum = 100
num = 0
for num in range(LoopNum):
    Pos_value = [300.5 + num ,-452.0, 366.4 , 179.5 ,- 0.8 , 175.7 , -1]
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    #print(ret)
    print("time:" + str(ret[0]))
    print("pos P,J:" + str(ret[1]))
    time.sleep(0.05)
for num in range(LoopNum):
    Pos_value = [300.5 + LoopNum - num , -452.0, 366.4 , 179.5 , -0.8 , 175.7 , -1]
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    #print(ret)
    print("time:" + str(ret[0]))
    print("pos P,J:" + str(ret[1]))
    time.sleep(0.05)
### Slave move: Change mode
Command = "slvChangeMode"  
Param = 0x000  # finish Slave Move  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))



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
