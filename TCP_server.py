import socketserver
import move
import os
import json

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.

    """

    def battery(self, battery_value):
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

    def handle(self):
        # self.request - TCP socket connected to the client
        command = self.request.recv(1024).strip().decode('utf-8')
        command_loaded = json.loads(command) #data loaded

        move_command = list(command_loaded.values())[0]
        parameter_one = list(command_loaded.values())[1]
        parameter_two = list(command_loaded.values())[2]
        battery_param = list(command_loaded.values())[3]

        if move_command == 'Auto_Run':
            move.Auto_Run()

        elif command == 'Emergency_Stop':
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
        print(self.battery(battery_param))
        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())




#  IP and PORT configuration is to be set up here
if __name__ == "__main__":
    HOST, PORT = "172.20.10.5", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()
