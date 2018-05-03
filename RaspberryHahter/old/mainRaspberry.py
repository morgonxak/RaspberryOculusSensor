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

connSesver = None


def parsData(data):
    #Pos,0,0,Mot,-3.470105,-25.13711
    data = data.split(',')
    return data

def sendServo(data):
    global x
    global y
    global oddPullArduino
    global Min_Servo_Camera, Max_Servo_Camera, Min_Servo_Platform, Max_Servo_Platform

    servoH = math.fabs(math.floor(float(data[2])))
    servoV = math.fabs(math.floor(float(data[1])))

    if (servoV >= Min_Servo_Camera) and (servoV <= Max_Servo_Camera):
        x = servoV
    if (servoH >= Min_Servo_Platform) and (servoH <= Max_Servo_Platform):
        y = servoH


    PullArduino = data[0]+' '+str(x)[:-2]+' '+str(y)[:-2]
    if (oddPullArduino <> PullArduino):
        oddPullArduino = PullArduino
        print("PullArduino  "+PullArduino)
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
       nR = b'1'
    if int(mapSpeadH) == -1:
       SpeadRight = FIRST_1
       nR = b'2'
    if int(mapSpeadH) == 0:
       SpeadRight = 0
       nR = b'0'

    if (int(mapSpeadV) == 1):
       SpeadLeft = FIRST_1
       nL = b'1'
    if int(mapSpeadV) == -1:
       SpeadLeft = FIRST_1
       nL = b'2'
    if int(mapSpeadV) == 0:
       SpeadLeft = 0
       nL = b'0'
#Для второй сткорости
    if (int(mapSpeadH) == 2):
       SpeadRight = FIRST_2
       nR = b'1'
    if int(mapSpeadH) == -2:
       SpeadRight = FIRST_2
       nR = b'2'
    if int(mapSpeadH) == 0:
       SpeadRight = 0
       nR = b'0'

    if (int(mapSpeadV) == 2):
       SpeadLeft = FIRST_2
       nL = b'1'
    if int(mapSpeadV) == -2:
       SpeadLeft = FIRST_2
       nL = b'2'
    if int(mapSpeadV) == 0:
       SpeadLeft = 0
       nL = b'0'

#Для третей скорости
    if (int(mapSpeadH) == 3):
       SpeadRight = FIRST_3
       nR = b'1'
    if int(mapSpeadH) == -3:
       SpeadRight = FIRST_3
       nR = b'2'
    if int(mapSpeadH) == 0:
       SpeadRight = 0
       nR = b'0'

    if int(mapSpeadV) == 3:
       SpeadLeft = FIRST_3
       nL = b'1'
    if int(mapSpeadV) == -3:
       SpeadLeft = FIRST_3
       nL = b'2'
    if int(mapSpeadV) == 0:
       SpeadLeft = 0
       nL = b'0'

    getArduino = data[3] + ' ' + nR + nL + str(SpeadRight) + str(SpeadLeft)

    if (oddGetArduino <> getArduino):
        oddGetArduino = getArduino
        driv.sendArduino(getArduino) #Отправить данные на Arduino
    if (data[6] == b"1"):
        driv.sendArduino("Mot00".encode())

def sendSensor():
    data = driv.GetSensotArduino("D")
    #print("data = " + data)
    return data


def mainLoop():
    global connSesver
    while 1:
        data = clien.getDataServer(connSesver)
        #print("Data = " + data)
        if data == "Dat":
            data = sendSensor()
            connSesver.send(data.encode())
        else:
            data = parsData(data)
            sendServo(data)
            sendMotor(data)


if __name__ == '__main__':  # Program start from here
    try:
        connSesver = clien.ConnectServer()
        mainLoop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        connSesver.close()
        print("Stop Client")
