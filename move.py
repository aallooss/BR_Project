import inspect
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


# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# Set the first direction you want it to spin
GPIO.output(DIR, CW)




#when function is called, the name of the function inside is printed, helpful for debugging and... logging
def log_call():
    print(inspect.stack()[1][3])

#Place individual code within these functions. The names are important as they are placed in 'app.py'
#some of these functions can be likely be refactored to accept paramenter for ex. one function to 
#change direction rather than two seperate functions
def Auto_Run():

    servo = AngularServo(12, min_pulse_width=.0006, max_pulse_width=0.0023)
    servo2 = AngularServo(20, min_pulse_width=.0008, max_pulse_width=0.0022)
    a= 1;
    b = 0;
    while (a < 5):
        servo.angle = -90
        sleep(.5)
        servo.value = None;
        sleep(.5)
        servo2.angle = -90                          
        sleep(.5)
        servo2.value = None; 
        sleep(1)
        servo.angle = 0
        sleep(.5)
        servo.value = None;
        sleep(.5)
        servo2.angle = 90
        sleep(.5)
        servo2.value = None;
        sleep(.5)
        sleep(1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           )
        a = a + 1
        print(a)
        if (a == 4):
            break; 
        elif (b == 1):
            break;
    servo.value = None;
    servo2.value = None;
    log_call()
    
def Emergency_Stop():
    log_call()
    
def feed_Hold():		
    log_call()
    
def Calibrate():	
    log_call()
    
def Jog_Z_positive():
    log_call()
    try:
        # Run forever.
        while True:

            """Change Direction: Changing direction requires time to switch. The
            time is dictated by the stepper motor and controller. """
            sleep(1.0)
            # Esablish the direction you want to go
            GPIO.output(DIR,CW)

            # Run for 200 steps. This will change based on how you set you controller
            for x in range(2000):

                # Set one coil winding to high
                GPIO.output(STEP,GPIO.HIGH)
                # Allow it to get there.
                sleep(.00005) # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(STEP,GPIO.LOW)
                sleep(.00005) # Dictates how fast stepper motor will run

            """Change Direction: Changing direction requires time to switch. The
            time is dictated by the stepper motor and controller. """
            sleep(1.0)
            GPIO.output(DIR,CCW)
            for x in range(2000):
                GPIO.output(STEP,GPIO.HIGH)
                sleep(.00005)
                GPIO.output(STEP,GPIO.LOW)
                sleep(.00005)

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()
        log_call()
    
def Jog_Z_negative():	
    log_call()
    
def Close_Gripper():	
    log_call()

def Open_Gripper():	
    log_call()

def Gripper_Yaw_CW():	
    log_call()

def Gripper_Yaw_CounterCW():	
    log_call()
