import socket
import json

host_ip, server_port = "127.0.0.1", 9999
data = {'Move_Commmand'     : 'Auto_Run',
        'Parameter_One'     : 'adf',            # None value if not needed
        'Parameter_Two'     : 'asdfadsf',       # None value if not needed
        'Battery_Param'     : 'adfadf0'}        # battery api in progress

data_string = json.dumps(data) #data serialized

# Initialize a TCP client socket using SOCK_STREAM
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Establish connection to TCP server and exchange data
    tcp_client.connect((host_ip, server_port))
    tcp_client.sendall(data_string.encode())

    # Read data from the TCP server and close the connection
    received = tcp_client.recv(1024)
finally:
    tcp_client.close()

print ("Move Command Sent:      {}".format(data_string[1]))
print ("Bytes Received:         {}".format(received.decode()))