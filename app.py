import json
from flask import Flask, escape, render_template, request, url_for, jsonify


#contains movement commands to GPIO
import move

#application must be name for AWS
application = Flask(__name__)

#root page routing
@application.route('/')
def index():
    return render_template('index.html')

#about page routing
@application.route('/about')
def about():
    return render_template('about.html')




# no parameter endpoints
@application.route('/api/no_parameter')
def access_param():
	move_command = request.args.get('move_command')
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
					'Battery'     :battery.get_battery_life()})

# one parameter endpoints
@application.route('/api/one_parameter')
def one_param_access_param():
	move_command = request.args.get('move_command')
	parameter = request.args.get('parameter')
	if move_command == 'gripper':
		move.gripper(parameter)		# direction
	elif move_command == 'end_effector_yaw':
		move.End_Effector_Yaw(parameter)
	else:
		return jsonify({'ERROR': 'invalid parameter'})
	return jsonify({'Move Command':source,
					'Direction'   :command,
					'Battery'     :battery.get_battery_life()})


# two parameter endpoints
@application.route('/api/two_parameter')
def two_param_access_param():
	parameter_one = request.args.get('parameter_one')
	parameter_two = request.args.get('parameter_two')
	move.Jog_Z(paramter_one, paramter_two)		#steps, direction
	return jsonify({'Move Command':'Jog Z',
					'Steps'       :parameter_one,
					'Direction'   :parameter_two,
					'Battery'     :battery.get_battery_life()})

# get only battery info
@application.route('/battery_info')
def two_param_access_param():
	return jsonify({'Percent'			:'Percent',
					'Current'       	:'Current',
					'Voltage'   		:'Voltage',
					'Charging status'   :'Charging status',
					'battery range'		:'range',
					'get battery shell'	:'battery shell',
					'shutdown level'    :'level',
					'shutdown delay'	:'delay',
					'chip temp'			:'temp'})

#HMI page routing
@application.route('/HMI', methods=["POST","GET"])
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

		#ignore this commented code below as it maybe be helpful for refactoring later if we so chose. 
		# button_name_imm_dict = request.form.to_dict()
		# button_name_str = list(button_name_imm_dict.values())[0]
		# move.Emergency_Stop()
		# move.auto_run()
		
		return render_template('HMI.html')
	elif request.method == 'GET':
		return render_template('HMI.html')

#MAIN
if __name__ == '__main__':
    application.run(host='192.168.0.102', debug=True) # flask run --host=0.0.0.0 to run on LAN
	#yerrrrrrrr