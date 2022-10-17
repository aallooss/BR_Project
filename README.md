# Mechatronics Senior Design Project

## Kennesaw State University X B&R Automation

## How to start

The second way is to manually clone this repository and change it later by own. Project is ready to run (with some requirements). You need to clone and run:

```sh
$ mkdir BR_Project
$ cd BR_Project
$ git clone https://github.com/aallooss/BR_Project.git
```

## Requirements

If you never worked with python projects then the simplest way is run project inside a virtual environment.

If you familiar with web development then you need Python, Flask and other dependencies.
Please follow the tutorial below to set up your evironment and com back when complete if not already installed.

- Working [`virtualenv`](https://python.land/virtual-environments/virtualenv) command

Welcome back.

Install the required dependencies in your cirtual environment using the command below:

```sh
pip install -r requirements.txt
```

## Windows

note: must be using Comment Prompt, not Powershell.

```sh
C:\Users\user\BR_Project> set FLASK_APP=app.py
C:\Users\user\BR_Project> flask run
```

## GNU/Linux

```sh
$ set FLASK_APP=app.py
$ flask run
```

## macOS

How to make full Python setup on macOS is not topic that can be cowered quickly (because you will need XCode and few more steps). One of the preferred ways to install required packages is to use `brew`. Memcached and Redis are not necessary for all sites, but I have included them in the project since my projects usually depend on them. If you need them also then install [`brew`](http://brew.sh) and then run this command:

```sh
$ set FLASK_APP=app.py
$ flask run
```

## Viewing website

Open http://127.0.0.1:5000/, customize project files and **have fun**. There will be a link given to you in the terminalm click that link to view the site on your local machine.

## Project structure

After you check out this code you may need to rename folder `BR_Project` to something more relevant your needs. I prefer to have own name for each project. Next step to change all mentions of the word `BR_Project` in your code. I don't add any code generators for this project since anyway make code reviews every time starting new Flask project by adding or removing extensions or some parts of the source code.

    .
    ├── BR_Project

Your Project file should look something like this.

    ├───Scripts         # should be generated when you create your virtual environment
    ├───static          # static files self
    │   ├───assets      # here are the jpg, png etc. files
    │   ├───css         # Bootstrap 5 here aswell as custom css
    │   └───js          # javascript
    ├───templates       # html here
    └───__pycache__     # created by python dont touch

# MISC

## Majority of the writing of code will be done in the files below:

    app.py

This is the core off the site. It routes all the pages and connects the front end to the backend.

    move.py

Here contains all the movements to the GPIO pins

# REST API

All of the following endpoints return a json dictionary page with the inputted parameters.

For PLC usage there are a collection of endpoints. There are three base movement functions:

* No parameter
* Two parameter
* Three paramer
* battery:&nbsp;&nbsp;True | False

The no parameter can be requested as such

## No paramter

> <robot_ip>:5000/api/no_parameter?move_command="move command"&battery="True/False"

The available commands are the following:

* auto_run
* emergency_stop
* feedhold
* calibrate
* battery:&nbsp;&nbsp;True | False

## One parameter

> <robot_ip>:5000/api/one_parameter?move_command="move command"&parameter="direction command"&battery="True/False"

The available move commands with there respective direction commands are the following:

* gripper: &nbsp;&nbsp; open | close
* end_effector_yaw: &nbsp;&nbsp; clockwise | counterclockwise
* battery:&nbsp;&nbsp;True | False

## Two parameter

> <robot_ip>:5000/api/two_parameter?parameter_one="command 1"&parameter_two="command2"&battery="True/False"

This endpoint only calls one function but takes integers as parameter unlike the previous. It always calls the Z Jog command and takes command1 as steps and command2 and direction.

* command1:&nbsp;&nbsp;0-~10000            // 3000 is around one inch of travel
* command2:&nbsp;&nbsp;0 = CW, &nbsp;&nbsp;1 = CCW
* battery:&nbsp;&nbsp;True | False

## Battery Only

> <robot_ip>:5000/api/battery_info

There is no customizable paramters for this endpoint, it will return the following JSON:
```json
data = {'Battery Percent'  :  float,
        'Battery Current'  :  float,
        'Battery Voltage'  :  float,
        'Battery Charging' :  float
        }
   
```

# TCP Socket

The TCP Socket provides a little more flexability. The server accepts a JSON as input, the most basic data is below and a helpful table can be found below.
```json
data = {
        'Move_Commmand'         : 'Auto_Run',
        'Parameter_One'         : None,
        'Parameter_Two'         : None,
        'Battery_Subscribe'     : None
        }
```


|  Move_Command  |  Parameter_One  |  Paramter_Two  | Battery Subscribe |
| :------------: | :-------------: | :-------------: | :---------------: |
|    Auto_Run    |      None      |      None      |    True/False    |
| Emergency_Stop |      None      |      None      |    True/False    |
|   Feed_Hold   |      None      |      None      |    True/False    |
|   Calibrate   |      None      |      None      |    True/False    |
|     Jog_Z     | 1-10000 (steps) | 0/1 (direction) |    True/False    |
|    Gripper    |   close/open   |      None      |    True/False    |
|  Gripper_Yaw  |     CW/CCW     |      None      |    True/False    |
