import subprocess
import re

def get_battery_subscription(battery_value):
    if battery_value == True:
        percent = subprocess.check_output('echo "get battery" | nc -q 0 127.0.0.1 8423', shell=True)
        current = subprocess.check_output('echo "get battery_i" | nc -q 0 127.0.0.1 8423', shell=True)
        voltage = subprocess.check_output('echo "get battery_v" | nc -q 0 127.0.0.1 8423', shell=True)
        charging = subprocess.check_output('echo "get battery_charging" | nc -q 0 127.0.0.1 8423', shell=True)
        battery_dict = { 'Battery Subscription' : True,
                          'Battery Percentage'  :  re.sub(r'\n', '', percent.decode()[percent.decode().index(' ')+1:]),
                         'Battery Current (A)'  :  re.sub(r'\n', '', current.decode()[current.decode().index(' ')+1:]),
                         'Battery Voltage (V)'  :  re.sub(r'\n', '', voltage.decode()[voltage.decode().index(' ')+1:]),
                            'Battery Charging'  :  re.findall(': ([a-z]+)', charging.decode().lower())}
    elif battery_value == False:
        battery_dict = {'Battery Subscription' : 'Unsubscribed'}
    else:
        battery_dict = { 'ERROR' : 'invalid parameter'}
    return battery_dict



