#!/usr/bin/env python3

# socket.SOCK_DGRAM udp
# socket.SOCK_STREAM tcp
# Reference to this code https://www.techwithtim.net/tutorials/socket-programming/

import struct
import socket
import time

HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address 172.1.0.48
PORT = 13117        # Port to listen on (non-privileged ports are > 1023)
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)


def create_msg():
    magic_cookie = int('feedbeef', 16)
    message_type = int('2', 16)
    server_port = int(47980)
    return struct.pack('!III', magic_cookie, message_type, server_port)


def start_UDP_server():
    print(f"Server started, listening on IP address {HOST}")
    message = create_msg()
    start_time = 0
    while start_time < 30: #Todo change to 10 and handle timeout
        cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        cs.sendto(message, ('255.255.255.255', PORT))
        time.sleep(1)
        start_time += 1

# start_UDP_server()





    # server.listen()
    # while True:
    #     conn, addr = server.accept()
    #     thread = threading.Thread(target=handle_client, args=(conn, addr))
    #     thread.start()
    #     print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")




# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server_socket:
#     udp_server_socket.bind((HOST, PORT))
#     print("Server started, listening on IP address ", HOST)
#     magic_cookie = "{0:08b}".format(int("0xfeedbeef", 16))
#     message_type = "{0:08b}".format(int("0x2", 16))
#     server_port = "{0:08b}".format(int("BB6C", 16))  # 47980 port in hex is BB6C
#
#     message = magic_cookie + message_type + server_port
#     byte_message = str.encode(message)
#
#     udp_server_socket.sendall(byte_message)
#     conn, addr = udp_server_socket.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)
