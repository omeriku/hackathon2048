
import socket
import threading
import time
from Game import divide_to_groups

# HEADER = 64
PORT = 47980
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

teams = {}

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


def start_TCP_server():
    server.listen()
    print(f"This is TCP Server started, IP and Port {ADDR}")

    server.settimeout(20) #Todo lower to 10
    # future = now + out
    while 1:
        try:
            conn, addr = server.accept()
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
        welcome_msg = welcome_msg + g[1]
    welcome_msg += "Group 2:\n==\n"
    for g in two_group:
        welcome_msg = welcome_msg + g[1]
    welcome_msg += "\nStart pressing keys on your keyboard as fast as you can!!\n"
    print(welcome_msg)

# start_TCP_server()
