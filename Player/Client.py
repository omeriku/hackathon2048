#!/usr/bin/env python3
import msvcrt
import socket
import struct
import time

# HOST = '172.1.0.48'  # The server's hostname or IP address

PORT = 13117        # The port usedf by the server
FORMAT = 'utf-8'

def startPlayer():
    # run listener on port 13117 until connection found and start tcp
    while 1:
        start_Client_UDP()

def checkMessage(msg):
    try:
        unpacked_msg = struct.unpack('!IbH', msg)
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

    unpacked_msg = struct.unpack('!IbH', msg)
    server_addr = (addr[0], unpacked_msg[2])

    print("Received offer from", addr[0], ", attempting to connect...")
    startTCP(server_addr)


def startTCP(addr):
    try:
        # print("this is address ", ADDR)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)

        client.send("BAMBA".encode(FORMAT))

        print(client.recv(1024).decode(FORMAT))

        # print("client Type !!!!!!!!!!!!!!")
        now = time.time()
        future = now + 10
        # the game
        while time.time() < future:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                client.send(key)

        print("done sending")
        print(client.recv(1024).decode())
        print("Server disconnected, listening for offer requests...")

    except ConnectionResetError:
        print("Server offline... looking for new connection")
        return


startPlayer()


