#import json
from flask import Flask, escape, render_template, request, url_for, jsonify


#contains movement commands to GPIO
import move

# battery dictionary
import battery

#application must be name for AWS
app = Flask(__name__)

#root page routing
@app.route('/')
def index():
    return render_template('index.html')

#about page routing
@app.route('/about')
def about():
    return render_template('about.html')




# no parameter endpoints
@app.route('/api/no_parameter')
def access_param():
	move_command = request.args.get('move_command')
	battery_command = request.args.get('battery')
	if source == 'auto_run':
		move.Auto_Run()
	elif source == 'emergency_stop':
		move.Emergency_Stop()
	elif source == 'feedhold':
		move.feed_Hold()
	elif source == 'calibrate':
		move.Calibrate()
	else:
		return jsonify({'ERROR': 'invalid parameter'})
	return jsonify({'Move Command':source,
					'Battery'     :battery.get_battery_subcription(battery_command)})

# one parameter endpoints
@app.route('/api/one_parameter')
def one_param_access_param():
	move_command = request.args.get('move_command')
	parameter = request.args.get('parameter')
	battery_command = request.args.get('battery')
	if move_command == 'gripper':
		move.gripper(parameter)		# direction
	elif move_command == 'end_effector_yaw':
		move.End_Effector_Yaw(parameter)
	else:
		return jsonify({'ERROR': 'invalid parameter'})
	return jsonify({'Move Command':source,
					'Direction'   :command,
					'Battery'     :battery.get_battery_subcription(battery_command)})


# two parameter endpoints
@app.route('/api/two_parameter')
def two_param_access_param():
	parameter_one = request.args.get('parameter_one')
	parameter_two = request.args.get('parameter_two')
	battery_command = request.args.get('battery')
	move.Jog_Z(paramter_one, paramter_two)		#steps, direction
	return jsonify({'Move Command':'Jog Z',
					'Steps'       :parameter_one,
					'Direction'   :parameter_two,
					'Battery'     :battery.get_battery_subcription(battery_command)})

# get only battery info
@app.route('/api/battery_info')
def battery_info():
	battery_command == True
	return jsonify(battery.get_battery_subcription(battery_command))

#HMI page routing
@app.route('/HMI', methods=["POST","GET"])
def HMI():
	if request.method == 'POST':
		#names of these values are important as they coorespond to the button values on 'HMI.html'
		if request.form['submit_button'] == 'Auto Run':
			move.Auto_Run()

		elif request.form['submit_button'] == 'Emergency Stop':
			move.Emergency_Stop()

		elif request.form['submit_button'] == 'Feed Hold':
			move.Feed_Hold()		

		elif request.form['submit_button'] == 'Calibrate':
			move.Calibrate()	

		elif request.form['submit_button'] == 'Jog Z+':
			move.Jog_Z(3000,1)	
		elif request.form['submit_button'] == 'Jog Z-':
			move.Jog_Z(3000,0)	

		elif request.form['submit_button'] == 'Close Gripper':
			move.Gripper()	
		elif request.form['submit_button'] == 'Open gitGripper':
			move.Gripper()	

		elif request.form['submit_button'] == 'Gripper Yaw CW':
			move.End_Effector_Yaw()	
		elif request.form['submit_button'] == 'Gripper Yaw CCW':
			move.End_Effector_Yaw()
		else:
			pass
		
		return render_template('HMI.html')
	elif request.method == 'GET':
		return render_template('HMI.html')

#MAIN
if __name__ == '__main__':
    app.run(host='192.168.0.102', debug=True) # flask run --host=0.0.0.0 to run on LAN
	#yerrrrrrrr