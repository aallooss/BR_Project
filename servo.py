import RPi.GPIO as GPIO
from time import sleep
import time
from gpiozero import AngularServo
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

def servo():
    servoPIN = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.stop()
    GPIO.cleanup()


servo()