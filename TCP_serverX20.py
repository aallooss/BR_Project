import socketserver
import move
import os
import json
import subprocess
import battery

class Handler_TCPServer(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request - TCP socket connected to the client
        command = self.request.recv(1024).strip().decode('utf-8')
        print(command)
        command_loaded = json.loads(command) #data loaded

        print(command_loaded)
        command_loaded = list(command_loaded.values())[0]
        print(command_loaded)
        move_command = list(command_loaded.values())[0]
        parameter_one = list(command_loaded.values())[1]
        parameter_two = list(command_loaded.values())[2]
        battery_param = list(command_loaded.values())[3]
        print(move_command)
        
        if move_command == 'Auto_Run':
            move.Auto_Run()

        elif move_command == 'Emergency_Stop':
            move.Emergency_Stop()

        elif move_command == 'Feed_Hold':
            move.Feed_Hold()

        elif move_command == 'Calibrate':
            move.Calibrate()

        elif move_command == 'Jog_Z':
            move.Jog_Z(parameter_one, parameter_two)

        elif move_command == 'Gripper':
            move.Gripper(parameter_one)

        elif move_command == 'Gripper_Yaw':
            move.End_Effector_Yaw(parameter_one)
        else:
            print("ERROR: Invalid command")
        print(command_loaded)
        print(battery.get_battery_subscription(battery_param))
        message = str(battery.get_battery_subscription(battery_param))
        # just send back ACK for data arrival confirmation
        self.request.sendall(message.encode())




#  IP and PORT configuration is to be set up here
if __name__ == "__main__":
    HOST, PORT = "192.168.0.101", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    print("TCP server active")
    tcp_server.serve_forever()

#webcalable function, used for HMI button
def web_callable():
    HOST, PORT = "192.168.0.101", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()
