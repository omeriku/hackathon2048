#!/usr/bin/env python3
import struct
import socket
import time


HOST = socket.gethostbyname(socket.gethostname())
PORT = 13117        # Port to listen on (non-privileged ports are > 1023)
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
LISTENING_PORT = 5080
HEX_BASE = 16
TIME_TO_WAIT = 10
BROADCAST_IP = '255.255.255.255'


def create_msg():
    """
    creating message for broadcast
    """
    magic_cookie = int('feedbeef', HEX_BASE)
    message_type = int('2', HEX_BASE)
    server_port = int(LISTENING_PORT)
    return struct.pack('!IbH', magic_cookie, message_type, server_port)


def start_UDP_server():
    """
    sending broadcast message for ten seconds, one message per 1 second
    """
    print(f"Server started, listening on IP address {HOST}")
    message = create_msg()
    now = time.time()
    future = now + TIME_TO_WAIT
    while time.time() < future:
        cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        cs.sendto(message, (BROADCAST_IP, PORT))
        time.sleep(1)

