from flask import Flask, escape, render_template, request, url_for

import move

#application must be name for AWS
application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/HMI', methods=["POST","GET"])
def HMI():
	if request.method == 'POST':
		button_name_imm_dict = request.form.to_dict()
		button_name_str = list(button_name_imm_dict.values())[0]

		move.Emergency_Stop()


		return render_template('HMI.html')
	elif request.method == 'GET':
		return render_template('HMI.html')

if __name__ == '__main__':
    application.run(debug=True)