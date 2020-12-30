

#!/usr/bin/env python3

import socket
import struct

# HOST = '172.1.0.48'  # The server's hostname or IP address

# HOST = '192.168.50.174' #Todo change
import time
from msvcrt import getch

PORT = 13117        # The port used by the server
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# ADDR = (HOST, PORT)
print("Client started, listening for offer requests...")

def start_Client_UDP():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    correct = False
    msg, addr = None, None
    while not correct:
        client.bind(('', PORT))
        # client.listen()
        msg, addr = client.recvfrom(1024)
        correct = True #Todo check msg

    # client.connect(addr)
    print("Received offer from", addr[0], ", attempting to connect...")
    print(msg)
    unpacked_msg = struct.unpack('!III', msg)
    print(unpacked_msg)
    server_addr = (addr[0], unpacked_msg[2])
    print("Received offer from", server_addr, ", attempting to connect...")
    startTCP(server_addr)

def send(msg, sender):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (1024 - len(send_length))
    sender.send(send_length)
    sender.send(message)
    print(sender.recv(2048).decode(FORMAT))

def startTCP(addr):

    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    ADDR = addr
    print("this is address ", ADDR)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    send("Hello Kitty", client)

    print(client.recv(2048).decode(FORMAT))

    running = True
    print("client Type !!!!!!!!!!!!!!")
    now = time.time()
    future = now + 10
    while time.time() < future:
        key = getch()
        send(key, client)

    print(client.recv(1024).decode())







start_Client_UDP()



# send("Hello World!")
# send("Hello Everyone!")
# send("0xfeedbeef")

# magic_cookie = "{0:08b}".format(int("0xfeedbeef", 16))
# message_type = "{0:08b}".format(int("0x2", 16))
# server_port = "{0:08b}".format(int("BB6C", 16))  # 47980 port in hex is BB6C
#
# message_2 = magic_cookie + message_type + server_port
# byte_message = str.encode(message)


# mmm = create_msg()
# send(mmm)


# send(DISCONNECT_MESSAGE)



# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
#
# print('Received', repr(data))
