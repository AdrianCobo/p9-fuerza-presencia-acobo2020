#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import time
import threading

sensorPresencia = 16

flag1 = 0


def callbackSalir (senial, cuadro): # señal y estado cuando se produjo la interrup.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

def comportamiento (canal):
    print("Presencia detectada!!!!!!!!")


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensorPresencia, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    hilo1 = threading.Thread(target=GPIO.add_event_detect(sensorPresencia, GPIO.RISING,
      callback=comportamiento, bouncetime=100))
    hilo1.start()

    hilo1.join()
    signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C que limpia todos los hilos anteriores
    signal.pause() # esperamos por hilo/callback CTRL+C antes de acabar para que no se acabe solo el principal