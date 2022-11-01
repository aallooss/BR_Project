import inspect import time
import subprocess
import json
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD) #using physical pin numbers NOT "GPIOxx"

limit_pin = 11 # physical pin 11
GPIO.setup(limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DIR = 10 #physical pin 10
GPIO.setup(DIR, GPIO.OUT)

STEP = 8 # physical pin 8
GPIO.setup(STEP, GPIO.OUT)

servo_gripper = 32
GPIO.setup(servo_gripper, GPIO.OUT)

servo_yaw = 38
GPIO.setup(servo_yaw, GPIO.OUT)

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
    Calibrate()    # Always run calibrate
    Gripper('open')
    Jog_Z(3000,0)
    End_Effector_Yaw('CW')
    End_Effector_Yaw('CCW')
    Gripper('close')
    log_call()

def Emergency_Stop():
    subprocess.check_output('sudo shutdown now', shell=True) #shuts Pi down immediantly 
    log_call()

def Feed_Hold():
    log_call()

def Calibrate():
    log_call()
#    GPIO.setmode(GPIO.BOARD) # Set PHYSICAL
    while GPIO.input(limit_pin):
        print('...Calibrating...')
        Jog_Z(150,0)
    Jog_Z(300,1)
    print('...Finished...')
 #   GPIO.cleanup()

def Jog_Z(steps,direction):     # 0/1 used to signify clockwise or counterclockwise.
    log_call()
    # Setup pin layout on PI
#    GPIO.setmode(GPIO.BOARD)
    # Establish Pins in software

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
#    GPIO.cleanup()

def Gripper(direction):
    log_call()

    p = GPIO.PWM(server_gripper, 50)
    p.start(0)
    if direction == "close":
        for  i in range(0,181):
            sig=(i/18)+2
            p.ChangeDutyCycle(sig)
            sleep(0.003)
        print("CLOSED gripper")
    elif direction == "open":
        for i in range(180,-1,-1):
            sig=(i/18)+2
            p.ChangeDutyCycle(sig)
            sleep(0.003)
        print("OPENED gripper")
    else:
        print("ERROR: Gripper - check command spelling")
    p.stop()
  #  GPIO.cleanup()

def End_Effector_Yaw(direction):
    log_call()

    p = GPIO.PWM(servo_yaw, 50) # GPIO 17 for PWM with 50Hz
    p.start(0)
    if direction == "CW":
        for i in range(0,181):
            sig=(i/18)+2
            p.ChangeDutyCycle(sig)
            sleep(0.003)
    elif direction == "CCW":
        for i in range(180,-1,-1):
            sig=(i/18)+2
            p.ChangeDutyCycle(sig)
            sleep(0.003)
    else:
        print("ERROR: End_Effector_Yaw - check command spelling")
    p.stop()
   # GPIO.cleanup()

Calibrate()
