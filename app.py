from flask import Flask, escape, render_template, request, url_for

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
@application.route('/PLC_API')
def access_param():
	source = request.args.get('command')
	if source == 'auto_run':
		move.Auto_Run()
	elif source == 'emergency_stop':
		move.Emergency_Stop()
	elif source == 'feedhold':
		move.feed_Hold()
	elif source == 'calibrate':
		move.Calibrate()
	else:
		return '''<h1>Error please double check your endpoint</h1>'''
	return '''<h1>The source value is: {}</h1>'''.format(source)

# one parameter endpoints
@application.route('/PLC_API_1')
def one_param_access_param():
	move_command = request.args.get('move_command')
	command = request.args.get('command')
	if move_command == 'gripper':
		move.gripper(command)		# direction
	elif move_command == 'end_effector_yaw':
		move.End_Effector_Yaw(command)
	else:
		return '''<h1>Error please double check your endpoint</h1>'''
	return '''<h1>The source value is: {}</h1>'''.format(command)


# two parameter endpoints
@application.route('/PLC_API_2')
def two_param_access_param():
	command1 = request.args.get('command1')
	command2 = request.args.get('command2')
	move.Jog_Z(command1, command2)		#steps, direction
	return '''<h1>The source values are : {}, {}<h1>'''.format(command1, command2)



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
			move.feed_Hold()		

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