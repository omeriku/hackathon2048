#!/usr/bin/env python3

# socket.SOCK_DGRAM udp
# socket.SOCK_STREAM tcp
# Reference to this code https://www.techwithtim.net/tutorials/socket-programming/

import struct
import socket
import time
# from scapy.arch import get_if_addr

HOST = socket.gethostbyname(socket.gethostname())  # Standard loopback interface address 172.1.0.48
# HOST = get_if_addr('eth1')
PORT = 13117        # Port to listen on (non-privileged ports are > 1023)
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)


def create_msg():
    magic_cookie = int('feedbeef', 16)
    message_type = int('2', 16)
    server_port = int(5080)
    return struct.pack('!IbH', magic_cookie, message_type, server_port)


def start_UDP_server():
    print(f"Server started, listening on IP address {HOST}")
    message = create_msg()
    now = time.time()
    future = now + 10
    while time.time() < future: #Todo change to 10 and handle timeout
        cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        cs.sendto(message, ('255.255.255.255', PORT))
        # print("BROADCAST Now")
        time.sleep(1)

