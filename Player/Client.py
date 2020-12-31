#!/usr/bin/env python3
import msvcrt
import socket
import struct
import time

# HOST = '172.1.0.48'  # The server's hostname or IP address

PORT = 13117        # The port used by the server
FORMAT = 'utf-8'
BUFFER_SIZE = 1024
TIME_TO_WAIT = 10


def startPlayer():
    """
    run listener on port 13117 until connection found and start tcp
    """""
    while 1:
        start_Client_UDP()

def checkMessage(msg):
    """

    :param msg: the message got from the UDP server
    :return: True - whether the message is valid by the format
    """
    try:
        unpacked_msg = struct.unpack('!IbH', msg)
        translated_msg = [hex(unpacked_msg[0]), hex(unpacked_msg[1]), unpacked_msg[2]]
        if str(translated_msg[0]) != "0xfeedbeef":
            return False
        elif str(translated_msg[1]) != "0x2":
            return False
        elif type(translated_msg[2]) is not int:
            return False
    except:
        return False
    return True

def start_Client_UDP():
    """
    listening to offer requests, and  if found and the message is valid then connect
    """
    print("Client started, listening for offer requests...")

    correct = False
    msg, addr = None, None
    while not correct:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        client.bind(('', PORT))
        msg, addr = client.recvfrom(BUFFER_SIZE)
        correct = checkMessage(msg)

        if not correct:
            client.close()

    unpacked_msg = struct.unpack('!IbH', msg)
    server_addr = (addr[0], unpacked_msg[2])

    print("Received offer from", addr[0], ", attempting to connect...")
    startTCP(server_addr)


def startTCP(addr):
    """
    :param addr: server address
    creating TCP connection to the server, send the team group name, play thee game and
    when finish the game and the server is disconnected.
    """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)

        client.send("BAMBA\n".encode(FORMAT))

        print(client.recv(BUFFER_SIZE).decode(FORMAT))

        now = time.time()
        future = now + TIME_TO_WAIT
        # the game
        while time.time() < future:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                client.send(key)

        print("done sending")
        print(client.recv(BUFFER_SIZE).decode())
        print("Server disconnected, listening for offer requests...")

    except ConnectionResetError:
        print("Server offline... looking for new connection")
        return


startPlayer()


