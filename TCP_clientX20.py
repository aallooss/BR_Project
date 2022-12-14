import socket
import json

host_ip, server_port = "192.168.0.100", 8888

# Initialize a TCP client socket using SOCK_STREAM
def CLIENT_SEND(feedback, calibration):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # commented out due to PLC formatting
    '''
    data = {'EZ3micro Command Completed' : feedback,
            'Calibration state'          : calibration}
    data_string = json.dumps(data) #data serialized
    '''

    # for X20 PLC use format below:
    # needs outer dict and no spaces since it parses keys as variables in PLC
    outer_dict = dict()
    data = {'move_command'      : feedback,
            'calibration_state' : calibration}
    outer_dict['data'] = data
    data_string = json.dumps(outer_dict) # data serialized


    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host_ip, server_port))
        tcp_client.sendall(data_string.encode())

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
#        tcp_client.shutdown(socket.SHUT_RD)
        tcp_client.close()
    print ("Move Command Sent:      {}".format(data))
    print ("Bytes Received:         {}".format(received.decode()))
