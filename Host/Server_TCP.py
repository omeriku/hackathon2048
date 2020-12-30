import signal
import socket
import threading
import time

from Game import *
from Player.Server_UDP import start_UDP_server
from threading import Thread

# HEADER = 64
PORT = 5080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
START_MESSAGE = ""
score_dict = {}
final_text = ""
def handle_client(conn, addr, teams, event):

    try:

        print(f"[NEW CONNECTION] {addr} connected.") #Todo delete prints
        name = conn.recv(1024).decode(FORMAT)

        print(f"[{addr}] {name}")
        teams[addr] = name
        # conn.send()
        conn.send((f"Your Team {name} in the game").encode(FORMAT))
        global score_dict
        score_dict[addr] = 0

        event.wait()
        conn.send(START_MESSAGE)

        now = time.time()
        future = now + 10
        # conn.settimeout(10)
        print("GAME START TYPE !!!!!!")
        # while time.time() < future:
        while 1:
            try:
                conn.settimeout(future-time.time())
                data = conn.recv(1024).decode(FORMAT)
                # print("received", data)
                score_dict[addr] += 1
            except:
                break
        print("!!!!!!!!!!! done receiving !!!!!!!!!!!!!!!!!")

        event.wait()
        conn.send(final_text.encode(FORMAT))

        # conn.send((f"The Game is over thank you {name}").encode(FORMAT))
        conn.close()
    except ConnectionResetError:
        print("client ", addr, "disconnected...")

def startAllServers():
    print(f"This is TCP Server started, IP and Port {ADDR}")
    while 1:
        t_tcp = Thread(target=start_TCP_server)
        t_udp = Thread(target=start_UDP_server)

        t_udp.start()
        t_tcp.start()

        t_udp.join()
        t_tcp.join()

def start_TCP_server():
    teams = {}
    all_clients = []
    global score_dict
    score_dict = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    server.settimeout(10)

    event = threading.Event()

    while 1:
        try:
            conn, addr = server.accept()
            all_clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr, teams, event))
            thread.start()
            print(f"\n[ACTIVE CONNECTIONS] {len(all_clients)}")
        except:
            print("done waiting for client")
            break
            # server.close()

    one_group, two_group = divide_to_groups(all_teams=teams)

    welcome_msg = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    for g in one_group:
        welcome_msg = welcome_msg + g[1] + "\n"
    welcome_msg += "Group 2:\n==\n"
    for g in two_group:
        welcome_msg = welcome_msg + g[1] + "\n"
    welcome_msg += "\nStart pressing keys on your keyboard as fast as you can!!\n"
    # print(welcome_msg)

    global START_MESSAGE
    START_MESSAGE = welcome_msg.encode(FORMAT)

    if (len(all_clients) == 0):
        print("no one came ...")
        return

    event.set()  # now play

    time.sleep(10) #Todo change
    # event.set()
    global final_text
    final_text = calculate_game(one_group,two_group)
    event.set()
    # for c in all_clients:
    #     c.send(final_text.encode(FORMAT))
    #     c.close()

    print("Game over, sending out offer requests...")

def calculate_game(group_a, group_b):
    sumA=0
    sumB=0
    for team in score_dict.keys():
        if team in group_a:
            sumA += score_dict[team]
        else:
            sumB += score_dict[team]
    winner = ""
    list_winner = []
    if sumA > sumB:
        winner = "1"
        for g in group_a:
            list_winner.append(g[1])
    elif sumA < sumB:
        for g in group_b:
            list_winner.append(g[1])
        winner = "2"
    text_to_print = "Game over!\nGroup1 typed in " + str(sumA) + " characters. Group2 typed in " + str(sumB) + \
                    " characters.\n" + "Group" + winner + " wins!\n\nCongratulations to the winners\n=="

    for w in list_winner:
        text_to_print += w + "\n"
    return text_to_print

