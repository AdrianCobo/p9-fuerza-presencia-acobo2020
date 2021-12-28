#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import time
import threading

sensorPresencia = 16
sensorPresion = 20
ledRojo=2

flag1 = 0
StartTime = 0

def callbackSalir (senial, cuadro): # señal y estado cuando se produjo la interrup.
    pwm.ChangeDutyCycle(0)
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

def comportamiento (canal):
    print("Boton pulsado!!!!!!!!")
    global StartTime
    global flag1
    flag1 = 1
    StartTime = time.time()

def comportamiento2 (canal):
    global flag1
    StopTime = time.time()
    finaltime = 0
    StopTime = time.time()
    finaltime = StopTime-StartTime
    pwm.ChangeDutyCycle(0)
    if (finaltime < 30 and flag1 == 1):
        print("Presencia detectada!!!!!!!!")
        pwm.ChangeDutyCycle(100)
        time.sleep(1)
        pwm.ChangeDutyCycle(0)
    else:
        flag1 = 0
        print("presiona el boton")
        pwm.ChangeDutyCycle(0)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensorPresencia, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorPresion, GPIO.IN)
    GPIO.setup (ledRojo, GPIO.OUT)

    pwm = GPIO.PWM(ledRojo,100)
    pwm.start (0)

    hilo1 = threading.Thread(target=GPIO.add_event_detect(sensorPresion, GPIO.RISING,
      callback=comportamiento, bouncetime=200))
    hilo1.start()

    hilo2 = threading.Thread(target=GPIO.add_event_detect(sensorPresencia, GPIO.RISING,
      callback=comportamiento2, bouncetime=200))
    hilo2.start()

    hilo1.join()
    hilo2.join()
    signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C que limpia todos los hilos anteriores
    signal.pause() # esperamos por hilo/callback CTRL+C antes de acabar para que no se acabe solo el principal