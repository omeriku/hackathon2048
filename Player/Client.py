

#!/usr/bin/env python3

import socket
import struct

# HOST = '172.1.0.48'  # The server's hostname or IP address

# HOST = '192.168.50.174' #Todo change
import time
from msvcrt import getch

PORT = 13117        # The port usedf by the server
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# ADDR = (HOST, PORT)

def startPlayer():
    # run listener on port 13117 until connection found and start tcp
    while 1:
        start_Client_UDP()

def checkMessage(msg):
    try:
        unpacked_msg = struct.unpack('!Ibh', msg)
        translated_msg = [hex(unpacked_msg[0]), hex(unpacked_msg[1]), unpacked_msg[2]]
        if (str(translated_msg[0]) != "0xfeedbeef"):
            return False
        elif (str(translated_msg[1]) != "0x2"):
            return False
        elif (type(translated_msg[2]) is not int):
            return False
    except:
        return False
    return True

def start_Client_UDP():
    print("Client started, listening for offer requests...")

    correct = False
    msg, addr = None, None
    while not correct:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        client.bind(('', PORT))
        # client.listen()
        msg, addr = client.recvfrom(1024)
        correct = checkMessage(msg)

        if not correct:
            client.close()

    # client.connect(addr)
    print("Received offer from", addr[0], ", attempting to connect...")
    print(msg)
    unpacked_msg = struct.unpack('!Ibh', msg)
    print(unpacked_msg)
    server_addr = (addr[0], unpacked_msg[2])
    print("Received offer from", server_addr, ", attempting to connect...")

    startTCP(server_addr)

def send(msg, sender):
    message = msg.encode(FORMAT)
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (1024 - len(send_length))
    # sender.send(send_length)
    sender.send(message)
    print(sender.recv(1024).decode(FORMAT))

def startTCP(addr):
    try:
        FORMAT = 'utf-8'
        DISCONNECT_MESSAGE = "!DISCONNECT"
        ADDR = addr
        print("this is address ", ADDR)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)

        send("Hello Kitty", client)

        print(client.recv(1024).decode(FORMAT))

        running = True
        print("client Type !!!!!!!!!!!!!!")
        now = time.time()
        future = now + 10

        while time.time() < future:
            # key = getch()
            # client.send(key)
            client.send("a".encode())
            time.sleep(1)
        print("done sending")
        print(client.recv(1024).decode())
        print("Server disconnected, listening for offer requests...")

    except ConnectionResetError:
        print("Server offline... looking for new connection")
        return


startPlayer()



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
