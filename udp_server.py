import socket
import time

HOST = '127.0.0.1'
PORT_SC = 5001
PORT_C = 5002
MAX_PACKET_SIZE = 3*1276

# Bind Source port to socket
UDP_SC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_SC.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,MAX_PACKET_SIZE)
UDP_SC.bind((HOST, PORT_SC))

# Bind client port to socket
UDP_C = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_C.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,MAX_PACKET_SIZE)
UDP_C.bind((HOST, PORT_C))

client_connected = False

while True:
    source_data, addr_sc = UDP_SC.recvfrom(MAX_PACKET_SIZE)
    
    # Waiting to recieve data from source client
    if source_data:
        print(f'Source connected at port: {PORT_SC}')
        UDP_SC.sendto(b'source connected', addr_sc)

    if client_connected:
        UDP_C.sendto(source_data, addr_c)
    
    client_msg, addr_c = UDP_C.recvfrom(MAX_PACKET_SIZE)

    if client_msg == b'C':
        client_connected = True
        print(f'Client connected at port: {PORT_C}')
    elif client_msg == b'D':
        client_connected = False
        print('Client disconnected')
