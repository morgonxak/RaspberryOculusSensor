#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
from time import sleep
ser = None

#отправить данные на arduino
def sendDataArduino(data):
    ser.write(data)
    #print(data)

def ConnectArduino():
    global ser
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)
        print("/dev/ttyUSB0")
    except serial.SerialException:
        ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=2)
        print("/dev/ttyUSB1")


#Принять данные С Arduino
def getDataArduino():
    try:
        data = ser.readline(ser.in_waiting)
        return data
    except serial.SerialException:
        print("error --- getDataArduino")
        sleep(1)
        ConnectArduino()
        return ('15')

def GetSensotArduino(data):
    while True:
        sendDataArduino(data)
        sleep(0.1)
        res = getDataArduino()
        if (res != ''):
            return res[:-2]

def SendDataServo(servo1, servo2):
    try:
        ser.write('P' + chr(servo1) + chr(servo2))
    except serial.SerialException:
        print("error --- SendDataServo")
        sleep(1)
        ConnectArduino()

def SendDataMotor(n1,n2,spead1,spead2):
    try:
        ser.write('M' + chr(n1) + chr(n2) + chr(spead1) + chr(spead2))
    except serial.SerialException:
        print("error --- SendDataMotor")
        ConnectArduino()


def test():
    pass

ConnectArduino()

if __name__ == '__main__':  # Program start from here
    try:
        test()

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        ser.close()
        print("Stop Client")