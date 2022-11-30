import inspect
import socketserver
import move
import os
import json
import subprocess
import battery
import TCP_clientX20
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BOARD)

servo_gripper= 32
GPIO.setup(servo_gripper, GPIO.OUT)


timing = .0000000003

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
    for  i in grip:
       sig=(70/18)+2
       p.ChangeDutyCycle(sig)
       sleep(0.3)
       if i == 100:
         break
    Calibrate(1)
    return p.ChangeDutyCycle(sig)

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
            sig=(150/18)+2
            p.ChangeDutyCycle(sig)
            sleep(0.3)
            if i == 100:
               break
        print("OPENED gripper")
        return p.ChangeDutyCycle(0)
    elif direction == "close":
        grip= [0,100]
        for i in grip:
           sig=(50/18)+2
           p.ChangeDutyCycle(sig)
           sleep(0.3)
           if i == 100:
              break
        print("CLOSED gripper")
        return p.ChangeDutyCycle(0)
        
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

def test():
    log.call()
    Calibrate(0)
    Gripper('open')
    Calibrate(1)



class Handler_TCPServer(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request - TCP socket connected to the client
        command = self.request.recv(1024).strip().decode('utf-8')
        print(command)
        command_loaded = json.loads(command) #data loaded

        command_loaded = list(command_loaded.values())[0]
        print(command_loaded)
        move_command = list(command_loaded.values())[0]
        parameter_one = list(command_loaded.values())[1]
        parameter_two = list(command_loaded.values())[2]
        battery_param = list(command_loaded.values())[3]
        print(move_command)
        message = str(battery.get_battery_subscription(battery_param))
        self.request.sendall(message.encode())
        Calibration = None
        Is_ready = None
        if move_command == 'Auto_Run':
            Auto_Run()
        elif move_command == 'Auto_Run_A':
            if Auto_Run_A() == True:
                Calibration = "SUCCESS"
            else:
                Calibration = "FAILURE"
        elif move_command == 'Auto_Run_B':
            if Auto_Run_B() == True:
                Calibration = "SUCCESS"
                Is_ready = True
            else:
                Calibration = "FAILURE"
        elif move_command == 'Emergency_Stop':
            Emergency_Stop()

        elif move_command == 'Feed_Hold':
            Feed_Hold()

        elif move_command == 'Calibrate':
            Calibrate(parameter_one) # this parameter determines direction 1 = up, 0 = down

        elif move_command == 'Jog_Z':
            Jog_Z(parameter_one, parameter_two)

        elif move_command == 'Gripper':
            Gripper(parameter_one)

        elif move_command == 'Gripper_Yaw':
            End_Effector_Yaw(parameter_one)
        else:
            print("ERROR: Invalid command")
        print(command_loaded)
        print(battery.get_battery_subscription(battery_param))
        if Is_ready == True:
            TCP_clientX20.CLIENT_SEND("Ready", None)
        TCP_clientX20.CLIENT_SEND(move_command, Calibration)
        #message = str(battery.get_battery_subscription(battery_param))
        # just send back ACK for data arrival confirmation
        # self.request.sendall(message.encode())




#  IP and PORT configuration is to be set up here
if __name__ == "__main__":
    HOST, PORT = "192.168.0.103", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    print("TCP server active")
    Calibrate(1)
    p = GPIO.PWM(servo_gripper, 50)
    p.start(0)
    p.ChangeDutyCycle(150/18 +2)
    sleep(0.3)
    p.ChangeDutyCycle(0)
    TCP_clientX20.CLIENT_SEND("Ready", None)   
    
    move.Calibrate(0)
    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()

#webcalable function, used for HMI button
def web_callable():
    HOST, PORT = "192.168.0.101", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    print("TCP server active")
    Calibrate(0)
    TCP_clientX20.CLIENT_SEND("Ready", None)   

    move.Calibrate(0)
    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()
