import socketserver
#import move
import os
import json
import subprocess
#import battery

class Handler_TCPServer(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request - TCP socket connected to the client
        command = self.request.recv(1024).strip().decode('utf-8')
        command_loaded = json.loads(command) #data loaded

        print(command_loaded)
        #print(battery.get_battery_subscription(battery_param))
        #message = str(battery.get_battery_subscription(battery_param))
        # just send back ACK for data arrival confirmation
        self.request.sendall(message.encode())




#  IP and PORT configuration is to be set up here
if __name__ == "__main__":
    HOST, PORT = "172.20.10.2", 8888

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    print("TCP server active")
    tcp_server.serve_forever()

#webcalable function, used for HMI button
def web_callable():
    HOST, PORT = "192.168.0.102", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()
