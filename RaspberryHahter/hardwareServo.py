#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

#преобразует пределы
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Выстовить определенный градус на сервоприводе
def SendDataServo(x,y):

    x = map(x, 0, 180, 200, 400)
    y = map(y,0,180,150,500)
    #отправляем данные
    pwm.set_pwm(0, 0, int(x))
    pwm.set_pwm(1, 0, int(y))