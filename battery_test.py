import subprocess
import re
import csv
import move
from datetime import datetime
from time import sleep
import time


#current_time = time.strftime("%H:%M:%S", t)

filename = "test2.csv"
columns = ['time', 'percent','current','voltage','cycle']

cycle = 0
while True:
	t = time.localtime()

	percent = subprocess.check_output('echo "get battery" | nc -q 0 127.0.0.1 8423', shell=True)
	current = subprocess.check_output('echo "get battery_i" | nc -q 0 127.0.0.1 8423', shell=True)
	voltage = subprocess.check_output('echo "get battery_v" | nc -q 0 127.0.0.1 8423', shell=True)
	charging = subprocess.check_output('echo "get battery_charging" | nc -q 0 127.0.0.1 8423', shell=True)

#while True:
	current_time = time.strftime("%H:%M:%S", t)
	battery_dict = [current_time,
		re.sub(r'\n', '',percent.decode()[percent.decode().index(' ')+1:]),
		re.sub(r'\n', '',current.decode()[current.decode().index(' ')+1:]),
		re.sub(r'\n', '',voltage.decode()[voltage.decode().index(' ')+1:]),
		cycle ]


#while True:
	move.Auto_Run()

	with open(filename, 'a', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
#		csvwriter.writerow(columns)
		csvwriter.writerow(battery_dict[0:])
	cycle += 1

	sleep(3)
