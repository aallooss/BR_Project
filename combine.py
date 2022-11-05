import socketserver
import move
import os
import json
import subprocess
import battery
import socket
import time
class Handler_TCPServer(socketserver.BaseRequestHandler):
    
    def client(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("172.19.10.5",8888))
            sock.sendall(bytes("PI CLIENT DATA", "utf-8"))
            received = str(sock.recv(1024), "utf-8")
        print("Sent: from Pi Client")

    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        time.sleep(2)
        self.client("command completed")

        self.request.sendall(self.data.upper())




#  IP and PORT configuration is to be set up here
if __name__ == "__main__":
    HOST, PORT = "172.20.10.5", 9999

    # Init the TCP server object, bind it to the chosen HOST and PORT
    with socketserver.TCPServer((HOST, PORT), Handler_TCPServer) as server:


    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
        print("TCP server active")
        server.serve_forever()

