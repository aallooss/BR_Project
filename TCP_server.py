import socketserver
import move
import battery
import re
import json

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.

    """

    def handle(self):
        # self.request - TCP socket connected to the client
        command = self.request.recv(1024).strip().decode('utf-8')
        command_loaded = json.loads(command) #data loaded


        move_command = list(command_loaded.values())[0]
        parameter_one = list(command_loaded.values())[1]
        parameter_two = list(command_loaded.values())[2]

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

        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())




#  IP and PORT configuration is to be set up here
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()
