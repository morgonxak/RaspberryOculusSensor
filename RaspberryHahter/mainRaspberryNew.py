#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ClientRaspberry as clien

import hardwareServo as servo
import hardwareDriver as drive
import hardwareSensor as sensor

import StartCamera as camera
import math

#камера
Max_Servo_Camera = 180
Min_Servo_Camera = 0
#плтформа
Max_Servo_Platform = 180
Min_Servo_Platform = 0
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
oldData = 'P, 90, 90, M, 0, 0, 0'

#Парсим данные которые пришли с сервера
def parsData(data):
    global oldData
    #Data = P,88.31198,77.54085,M,0,0,0
    tempData = data
    data = data.split(',')
    if len(data) > 8 or len(data)<8:
       data = oldData
       data = data.split(',')
    else:
        oldData = tempData

    return data

#преобразует пределы
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Отправляем данные для серво приводав
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

    servo.SendDataServo(int(x), int(y)) #Отправляем данные на Arduino


def sendMotor(data):
    global oddGetArduino

   #Pos,0,0,Mot,-3.470105,-25.13711
    #P, 90, 90, M, 0, 0, 0
    nR = 0
    nL = 0
    SpeadRight = 0
    SpeadLeft = 0

    speadH = data[4]
    speadV = math.floor(float(data[5]))

    #mapSpeadH = map(speadH, -255, 255, -3, 3)
    #mapSpeadV = map(speadV, -255, 255, -3, 3)

    if speadH == b'1':
        nR = 1
        nL = 1
    elif speadH == b'2':
        nR = 1
        nL = 2
    elif speadH == b'3':
        nR = 2
        nL = 2
    elif speadH == b'4':
        nR = 2
        nL = 1
    else:
        nR = 0
        nL = 0
    print("speadH "+ speadH )
    print("nR = "+ str(nR)+ " nL = "+str(nL))
    SpeadLeft = FIRST_2
    SpeadRight = FIRST_2

    drive.SendDataMotor(nL,nR,SpeadLeft,SpeadRight)

    #print(str(nL)+" "+str(nR)+" "+str(SpeadLeft)+" "+str(SpeadRight))
    if (data[6] == b"1"):# данные на остановку
        #print("0 0 0 0")
        drive.SendDataMotor(0,0,0,0)

def sendSensor():
    #data = arduino.GetSensotArduino('D')
    data = str(sensor.getSensor(0))
    #print("data = " + data)
    return data


def mainLoop():
    global connSesver
    while 1:
        data = clien.getDataServer(connSesver)

        if data in 'D':
            #print("Запрос на данные")
            data = sendSensor()
            connSesver.send(data.encode())

        else:
            data = parsData(data)
            #print(data)
            sendServo(data)
            sendMotor(data)



if __name__ == '__main__':  # Program start from here
    try:
        connSesver = clien.ConnectServer()
        #camera.start()
        mainLoop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        connSesver.close()
        drive.destroy()
        #camera.stop()
        print("Stop Client")
