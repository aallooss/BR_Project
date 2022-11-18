import socket
import json

host_ip, server_port = "172.20.10.3", 9999
data = {'gx20PLC' :
                {'Move_Commmand'     : 'Auto_Run',
                 'Parameter_One'     : 0,         # None value if not needed
                 'Parameter_Two'     : 0,            # None value if not needed
             'Battery_Subscribe'     : 1}}        # battery api True/False to subscribe or unsubscribe
data_string = json.dumps(data)              # data serialized

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
print ("Move Command Sent:      {}".format(data))
print ("Bytes Received:         {}".format(received.decode()))