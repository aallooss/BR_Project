import inspect
import time
import RPi.GPIO as GPIO
from time import sleep
from gpiozero import AngularServo
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0






#when function is called, the name of the function inside is printed, helpful for debugging and... logging
def log_call():
    print(inspect.stack()[1][3])

#Place individual code within these functions. The names are important as they are placed in 'app.py'
#some of these functions can be likely be refactored to accept paramenter for ex. one function to 
#change direction rather than two seperate functions
def Auto_Run():
    log_call()
    
def Emergency_Stop():
    log_call()
    
def Feed_Hold():		
    log_call()
    
def Calibrate():
    log_call()
    
def Jog_Z(steps,direction):     # 0/1 used to signify clockwise or counterclockwise.
    log_call()
    # Setup pin layout on PI
    GPIO.setmode(GPIO.BOARD)
    # Establish Pins in software
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

    print(direction)
    # Esablish the direction you want to go
    GPIO.output(DIR,direction)
    # Run for 200 steps. This will change based on how you set you controller
    for x in range(steps):
        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        sleep(.00005) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        sleep(.00005) # Dictates how fast stepper motor will run
    GPIO.cleanup()


def Gripper():
    log_call()
    servoPIN = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    p.ChangeDutyCycle(12.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)

    GPIO.cleanup()



def End_Effector_Yaw():	
    log_call()
    servoPIN = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    p.ChangeDutyCycle(12.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)

    GPIO.cleanup()
