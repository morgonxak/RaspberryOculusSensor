#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
#from settings import GPIO,PIN_EN_A,PIN_EN_B,PIN_IN_1_A,PIN_IN_1_B,PIN_IN_2_A,PIN_IN_2_B
import time
import RPi.GPIO as GPIO
PIN_IN_1_A = 14  # pin11
PIN_IN_2_A = 17  # pin12
PIN_EN_A = 23  # pin13

PIN_IN_1_B = 27   # pin11
PIN_IN_2_B = 22  # pin12
PIN_EN_B = 24  # pin13

pwm = None

def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
    #GPIO.setwarnings(False)

    GPIO.setup(PIN_IN_1_A, GPIO.OUT)  # mode --- output motor A
    GPIO.setup(PIN_IN_2_A, GPIO.OUT)
    GPIO.setup(PIN_EN_A, GPIO.OUT)

    GPIO.setup(PIN_IN_1_B, GPIO.OUT)  # mode --- output motor B
    GPIO.setup(PIN_IN_2_B, GPIO.OUT)
    GPIO.setup(PIN_EN_B, GPIO.OUT)

    pwm_A = GPIO.PWM(PIN_EN_A,10)
    pwm_A.start(0)

    pwm_B = GPIO.PWM(PIN_EN_B, 10)
    pwm_B.start(0)

    return (pwm_A,pwm_B)


def go_forward(spead=50):
    pwm[0].ChangeDutyCycle(spead)
    pwm[1].ChangeDutyCycle(spead)

    GPIO.output(PIN_IN_1_A, GPIO.HIGH)  # clockwise
    GPIO.output(PIN_IN_2_A, GPIO.LOW)

    GPIO.output(PIN_IN_1_B, GPIO.HIGH)  # clockwise
    GPIO.output(PIN_IN_2_B, GPIO.LOW)
    #time.sleep(5)


def go_back(spead=50):
    pwm[0].ChangeDutyCycle(spead)
    pwm[1].ChangeDutyCycle(spead)

    GPIO.output(PIN_IN_1_A, GPIO.LOW)  # clockwise
    GPIO.output(PIN_IN_2_A, GPIO.HIGH)

    GPIO.output(PIN_IN_1_B, GPIO.LOW)  # clockwise
    GPIO.output(PIN_IN_2_B, GPIO.HIGH)



def go_left(spead_A=50,spead_B=50):
    pwm[0].ChangeDutyCycle(spead_A)
    pwm[1].ChangeDutyCycle(spead_B)

    GPIO.output(PIN_IN_1_A, GPIO.LOW)  # clockwise
    GPIO.output(PIN_IN_2_A, GPIO.HIGH)

    GPIO.output(PIN_IN_1_B, GPIO.HIGH)  # clockwise
    GPIO.output(PIN_IN_2_B, GPIO.LOW)



def go_right(spead_A=50,spead_B=50):
    pwm[0].ChangeDutyCycle(spead_A)
    pwm[1].ChangeDutyCycle(spead_B)

    GPIO.output(PIN_IN_1_A, GPIO.HIGH)  # clockwise
    GPIO.output(PIN_IN_2_A, GPIO.LOW)

    GPIO.output(PIN_IN_1_B, GPIO.LOW)  # clockwise
    GPIO.output(PIN_IN_2_B, GPIO.HIGH)

def stopMotor():
    GPIO.output(PIN_EN_A, GPIO.LOW)  # motor stop
    GPIO.output(PIN_EN_B, GPIO.LOW)

    pwm[0].stop()
    pwm[1].stop()

#преобразует пределы
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



def test():
    t = 0.1
    while True:
        go_forward()
        time.sleep(t)
        go_back()
        time.sleep(t)
        go_left()
        time.sleep(t)
        go_right()
        time.sleep(t)

def destroy(pwm):
    GPIO.output(PIN_EN_A, GPIO.LOW)  # motor stop
    GPIO.output(PIN_EN_B, GPIO.LOW)

    pwm[0].stop()
    pwm[1].stop()

    GPIO.cleanup()  # Release resource


def SendDataMotor(nL,nR,SR,SL):
    if nR == 0:
        GPIO.output(PIN_IN_1_B, GPIO.LOW)
        GPIO.output(PIN_IN_2_B, GPIO.LOW)
    elif nR == 1:
        GPIO.output(PIN_IN_1_B, GPIO.LOW)
        GPIO.output(PIN_IN_2_B, GPIO.HIGH)
    elif nR == 2:

        GPIO.output(PIN_IN_1_B, GPIO.HIGH)
        GPIO.output(PIN_IN_2_B, GPIO.LOW)

    if nL == 0:

        GPIO.output(PIN_IN_1_A, GPIO.LOW)
        GPIO.output(PIN_IN_2_A, GPIO.LOW)
    elif nL == 1:
        GPIO.output(PIN_IN_1_A, GPIO.LOW)
        GPIO.output(PIN_IN_2_A, GPIO.HIGH)
    elif nL == 2:
        GPIO.output(PIN_IN_1_A, GPIO.HIGH)
        GPIO.output(PIN_IN_2_A, GPIO.LOW)

    #Задаем скорость моторам
    pwm[0].ChangeDutyCycle(map(SL,0,255,0,100))
    pwm[1].ChangeDutyCycle(map(SR,0,255,0,100))

pwm = setup()

if __name__ == '__main__':  # Program start from here
    pwm = setup()
    try:
        test()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy(pwm)