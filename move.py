import inspect

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
    
def feed_Hold():		
    log_call()
    
def Calibrate():	
    log_call()
    
def Jog_Z_positive():	
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
