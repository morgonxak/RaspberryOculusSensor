#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ClientRaspberry as clien
import driving as driv
import math

#камера
Max_Servo_Camera = 180
Min_Servo_Camera = 30
#плтформа
Max_Servo_Platform = 180
Min_Servo_Platform = 30
Point_Ziro = 90

x = 90
y = 90
###
#Скорость передач моторов
FIRST_1 = 100
FIRST_2 = 160
FIRST_3 = 235

oddGetArduino = ''
oddPullArduino = ''


def parsData(data):
    #Pos,0,0,Mot,-3.470105,-25.13711
    data = data.split(',')
    return data

def sendServo(data):
    global x
    global y
    global oddPullArduino

    servoH = float(data[2])
    servoV = float(data[1])

    Point_Ziro_to_Left = math.floor(map(servoH,0,90,Point_Ziro,Max_Servo_Platform))
    Point_Ziro_to_Right = math.floor(map(servoH,0,-90,Point_Ziro,Min_Servo_Platform))

    Point_Ziro_to_Up = map(servoV,0,90,Point_Ziro,Max_Servo_Camera)
    Point_Ziro_to_Down = map(servoV,0,-90,Point_Ziro,Min_Servo_Camera)

    if servoH > 0:
        x = int(Point_Ziro_to_Left)
    else:
        x = int(Point_Ziro_to_Right)

    if servoV > 0:
        y = int(Point_Ziro_to_Up)
    else:
        y = int(Point_Ziro_to_Down)




    PullArduino = data[0]+' '+str(x)+' '+str(y)
    if (oddPullArduino <> PullArduino):
        oddPullArduino = PullArduino
        driv.sendArduino(PullArduino) #Отправить данные на Arduino


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def sendMotor(data):

    global oddGetArduino

   #Pos,0,0,Mot,-3.470105,-25.13711
    nR = 0
    nL = 0
    SpeadRight = 0
    SpeadLeft = 0

    speadH = math.floor(float(data[4]))
    speadV = math.floor(float(data[5]))

    mapSpeadH = map(speadH, -255, 255, -3, 3)
    mapSpeadV = map(speadV, -255, 255, -3, 3)

##Для первой скорости
    if (int(mapSpeadH) == 1):
       SpeadRight = FIRST_1
       nR = '1'
    if int(mapSpeadH) == -1:
       SpeadRight = FIRST_1
       nR = '-1'
    if int(mapSpeadH) == 0:
       SpeadRight = 0
       nR = '0'

    if (int(mapSpeadV) == 1):
       SpeadLeft = FIRST_1
       nL = '1'
    if int(mapSpeadV) == -1:
       SpeadLeft = FIRST_1
       nL = '-1'
    if int(mapSpeadV) == 0:
       SpeadLeft = 0
       nL = '0'
#Для второй сткорости
    if (int(mapSpeadH) == 2):
       SpeadRight = FIRST_2
       nR = '1'
    if int(mapSpeadH) == -2:
       SpeadRight = FIRST_2
       nR = '-1'
    if int(mapSpeadH) == 0:
       SpeadRight = 0
       nR = '0'

    if (int(mapSpeadV) == 2):
       SpeadLeft = FIRST_2
       nL = '1'
    if int(mapSpeadV) == -2:
       SpeadLeft = FIRST_2
       nL = '-1'
    if int(mapSpeadV) == 0:
       SpeadLeft = 0
       nL = '0'

#Для третей скорости
    if (int(mapSpeadH) == 3):
       SpeadRight = FIRST_3
       nR = '1'
    if int(mapSpeadH) == -3:
       SpeadRight = FIRST_3
       nR = '-1'
    if int(mapSpeadH) == 0:
       SpeadRight = 0
       nR = '0'

    if int(mapSpeadV) == 3:
       SpeadLeft = FIRST_3
       nL = '1'
    if int(mapSpeadV) == -3:
       SpeadLeft = FIRST_3
       nL = '-1'
    if int(mapSpeadV) == 0:
       SpeadLeft = 0
       nL = '0'

    getArduino = data[3] + ' ' + nR + ' ' + nL + ' ' + str(SpeadRight) + ' ' + str(SpeadLeft)

    if (oddGetArduino <> getArduino):
        oddGetArduino = getArduino
        driv.sendArduino(getArduino) #Отправить данные на Arduino
    if (data[6] == "1"):
        driv.sendArduino("Mot 0 0")

def sendSensor(conn):
    print("Зашол в условия Dat")

    data = driv.GetSensotArduino("Dat 0 0 0 0")

    print("data = " + data)
    conn.send(data)
    clien.DisconectServer(conn)


def mainLoop():
   while 1:
        conn = clien.ConnectServer()
        data = clien.getDataServer(conn)
        #print("Data = " + data)
        if data ==b"Dat":
            print("IF DAt ---- OK")
            sendSensor(conn)
        else:
            clien.DisconectServer(conn)
            data = parsData(data)
            #sendServo(data)


if __name__ == '__main__':  # Program start from here
    try:
        mainLoop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("Stop Client")
