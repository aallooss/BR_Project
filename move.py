import inspect
import time
import subprocess
import json
import RPi.GPIO as GPIO
from time import sleep
import TCP_serverX20

GPIO.setmode(GPIO.BOARD) #using physical pin numbers NOT "GPIOxx"

timing = .0000003

bottom_limit_pin = 11 # physical pin 11
GPIO.setup(bottom_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

top_limit_pin = 12
GPIO.setup(top_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DIR = 10 #physical pin 10
GPIO.setup(DIR, GPIO.OUT)

STEP = 8 # physical pin 8
GPIO.setup(STEP, GPIO.OUT)

servo_yaw = 38
GPIO.setup(servo_yaw, GPIO.OUT)

# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

#t_end = time.time() + 10 # 10 seconds for calibration before failure

#when function is called, the name of the function inside is printed, helpful for debugging and... logging
def log_call():
    print(inspect.stack()[1][3])

#Place individual code within these functions. The names are important as they are placed in 'app.py'
#some of these functions can be likely be refactored to accept paramenter for ex. one function to 
#change direction rather than two seperate functions
def Auto_Run():
    Calibrate(0)    # 0 is bottom limit
    Gripper('close')
    Jog_Z(10000,1)
    End_Effector_Yaw('CCW')
    End_Effector_Yaw('CW')
    Gripper('open')
    log_call()

def Auto_Run_A():
   log_call()
   Calibrate(0) # 0 is bottom limit
   Gripper('close')
   End_Effector_Yaw('CCW')
   return Calibrate(1)

def Auto_Run_B():
   log_call()
   End_Effector_Yaw('CW')
   Calibrate(0) # 0 is bottom limit
   Gripper('open')
   return Calibrate(1) # top limit

def Emergency_Stop():
    subprocess.check_output('sudo reboot', shell=True) #shuts Pi down immediantly 
    log_call()

def Feed_Hold():
    log_call()
    Calibrate(0)
    grip= [0,100]
    p=TCP_serverX20.p
    for  i in grip:
       sig=(100/18)+2
       p.ChangeDutyCycle(sig)
       sleep(0.3)
       if i == 100:
         break
    Calibrate(1)
    return p.ChangeDutycycle(sig)

def Calibrate(direction):
    log_call()
    if direction == 0: # bottom limit
        limit_pin = bottom_limit_pin
    elif direction == 1: # top limit
        limit_pin = top_limit_pin
    else:
        print("ERROR CHECK LIMIT PIN NUMBER")
        return False # returns false (failure) if pin number isnt set correctly

    t_end = time.time() + 10

    # if direction  if  0 then then it will calibrate to the bottom, 1 calibrate to top
    GPIO.output(DIR, direction) # set direction downward
    while time.time() < t_end and GPIO.input(limit_pin): # Calibation runs for 10 seconds defined by "t_end" if takes more time calibration returns false (failure)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(timing)
        GPIO.output(STEP, GPIO.LOW)
        sleep(timing)
    if GPIO.input(limit_pin) == True: # True means that the limit switch has not been enaged
        print("FAILURE: Calibration Timed out")
        return False
    GPIO.output(DIR, not direction)	# set direcion upward
    for i in range(300):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(timing)
        GPIO.output(STEP, GPIO.LOW)
        sleep(timing)
    print("...Calibrated...")
    return True



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
        sleep(timing) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        sleep(timing) # Dictates how fast stepper motor will run
        if GPIO.input(limit_pin) == 0:
            print('ERROR: limit reached')
            Calibrate(0)
            return
    # GPIO.cleanup()

def Gripper(direction):
    log_call()
    grip= [0,100]
    if direction == "open":
        for  i in grip:
            sig=(100/18)+2
            TCP_serverX20.p.ChangeDutyCycle(sig)
            sleep(0.3)
            TCP_serverX20.p.ChangeDutyCycle(0)
            if i == 100:
               break
        print("OPENED gripper")
    elif direction == "close":
        for i in range(181,-1,-1):
            sig=(i/18)+2
            TCP_serverX20.p.ChangeDutyCycle(sig)
            sleep(0.003)
        print("CLOSED gripper")
    else:
        print("ERROR: Gripper - check command spelling")
    TCP_serverX20.p.stop()
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

def test():
    log.call()
    Calibrate(0)
    Gripper('open')
    Calibrate(1)

