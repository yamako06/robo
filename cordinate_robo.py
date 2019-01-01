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
x_new=[]
J1_new=[]
J2_new=[]
J3_new=[]
J4_new=[]
J5_new=[]
J6_new=[]
x_point=[]
J1_pos=[]


###補間用関数
def get_interpolate_data(x, y, num, kind):
    f_CS = interp1d(x, y, kind=kind)
    x_new = np.linspace(0, np.pi, num=num)[::-1]
    x_new = np.min(x) + (1 + np.cos(x_new)) * (np.max(x) - np.min(x)) /2
    y_new = f_CS(x_new)      
    return np.round(y_new,5)

###補間後ポジションデータの格納（P）
def Pos(P,pos):
    curpos=[]
    for i in range(P-1,P+1):
        if P!=0:
            curpos.append(pos[i])
        elif P ==0:
            curpos.append(pos[i+1])
    return curpos

###座標格納関数
def get_move_pos(J_pos,J1,J2,J3,J4,J5,J6,Loopnum):
    J_pos[0]=str(J1[Loopnum])
    J_pos[1]=str(J2[Loopnum])
    J_pos[2]=str(J3[Loopnum])
    J_pos[3]=str(J4[Loopnum])
    J_pos[4]=str(J5[Loopnum])
    J_pos[5]=str(J6[Loopnum])
    return J_pos


###入力データ
csvfile = 'SRC_comp.csv'
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
'リスト内をfloatに変換'
J1=list(map(float, J1))
J2=list(map(float, J2))
J3=list(map(float, J3))
J4=list(map(float, J4))
J5=list(map(float, J5))
J6=list(map(float, J6))

cnt1 = 0.005
Pos_value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
f=open('output.csv','w')
writer = csv.writer(f, lineterminator='\n')


###関数
'point番号'
for P in range(10):
    csvlist=[]
    x_new=Pos(P,x)
    J1_new=Pos(P,J1)
    J2_new=Pos(P,J2)
    J3_new=Pos(P,J3)
    J4_new=Pos(P,J4)
    J5_new=Pos(P,J5)
    J6_new=Pos(P,J6)

    ##初期入力
    '始点から終点まで何点で表すか'
    LoopNum =5
    'スプライン補間方法選択'
    #kind = "cubic"
    kind = "slinear"
    '補間関数実行'
    J1_new = get_interpolate_data(x_new, J1_new, LoopNum, kind)
    J2_new = get_interpolate_data(x_new, J2_new, LoopNum, kind)
    J3_new = get_interpolate_data(x_new, J3_new, LoopNum, kind)
    J4_new = get_interpolate_data(x_new, J4_new, LoopNum, kind)
    J5_new = get_interpolate_data(x_new, J5_new, LoopNum, kind)
    J6_new = get_interpolate_data(x_new, J6_new, LoopNum, kind)
    for num in range(LoopNum):
        Pos_value = get_move_pos(Pos_value,J1_new,J2_new,J3_new,J4_new,J5_new,J6_new,num)
        print(P,Pos_value)
        time.sleep(cnt1)
        writer.writerow(Pos_value)
         
 
f.close()



"""戻るときに使用    
for num in range(LoopNum):
    Pos_value =  get_move_pos(Pos_value,y_new,J_num,LoopNum-num)
    print(Pos_value)
    time.sleep(cnt1)
"""

print("Finish")