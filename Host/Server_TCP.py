
import socket
import threading
import time

from Game import divide_to_groups
from Player.Server_UDP import start_UDP_server
from threading import Thread

# HEADER = 64
PORT = 47980
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"



teams = {}
all_clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.") #Todo delete prints

    # connected = True
    # while connected:
    msg_length = conn.recv(1024).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        name = conn.recv(msg_length).decode(FORMAT)

        print(f"[{addr}] {name}")
        teams[addr] = name
        conn.send((f"Your Team {name} in the game").encode(FORMAT))

    # conn.close()

def startGame():
    print(f"This is TCP Server started, IP and Port {ADDR}")
    while 1:
        t_tcp = Thread(target=start_TCP_server)
        t_udp = Thread(target=start_UDP_server)

        t_tcp.start()
        t_udp.start()

        t_udp.join()
        t_tcp.join()

def start_TCP_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    server.settimeout(10) #Todo lower to 10
    # future = now + out
    while 1:
        try:
            conn, addr = server.accept()
            all_clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount() - 3}")
        except socket.timeout as e:
            print("done waiting for players")
            server.close()

            break

    one_group, two_group = divide_to_groups(all_teams=teams)

    welcome_msg = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    for g in one_group:
        welcome_msg = welcome_msg + g[1] + "\n"
    welcome_msg += "Group 2:\n==\n"
    for g in two_group:
        welcome_msg = welcome_msg + g[1] + "\n"
    welcome_msg += "\nStart pressing keys on your keyboard as fast as you can!!\n"
    # print(welcome_msg)

    message = welcome_msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (1024 - len(send_length))

    for group in all_clients:
        # server.sendto(send_length, group)
        group.send(message)
    print("now the game")
    time.sleep(15)

    print("15 sec over")



# start_TCP_server()
