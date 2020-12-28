#!/usr/bin/env python3

# socket.SOCK_DGRAM udp
# socket.SOCK_STREAM tcp

import socket

HOST = '172.1.0.48'  # Standard loopback interface address (localhost)
PORT = 13117        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server_socket:
    udp_server_socket.bind((HOST, PORT))
    print("Server started, listening on IP address ", HOST)
    magic_cookie = "{0:08b}".format(int("0xfeedbeef", 16))
    message_type = "{0:08b}".format(int("0x2", 16))
    server_port = "{0:08b}".format(int("BB6C", 16))  # 47980 port in hex is BB6C

    message = magic_cookie + message_type + server_port
    byte_message = str.encode(message)

    udp_server_socket.sendall(byte_message)
    conn, addr = udp_server_socket.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
