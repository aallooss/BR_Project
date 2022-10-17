def get_battery_subcription(battery_value):
    if battery_value == True:
        battery_dict = { 'Battery Percent'  :  os.system(' echo "get battery" | nc -q 0 127.0.0.1 8423 '),
                            'Battery Current'  :  os.system(' echo "get battery_i" | nc -q 0 127.0.0.1 8423 '),
                            'Battery Voltage'  :  os.system(' echo "get battery_v" | nc -q 0 127.0.0.1 8423 '),
                            'Battery Charging' :  os.system(' echo "get battery_charging" | nc -q 0 127.0.0.1 8423 ')}
    elif battery_value == False: 
        battery_dict = {'Battery Subscritption' : 'Unsubscribed'}
    else:
        battery_dict = {'Battery Subscrption'   : 'ERROR'}
    return battery_dict