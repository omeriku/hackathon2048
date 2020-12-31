import socket
import threading
import time
import random
from Player.Server_UDP import start_UDP_server
from threading import Thread


PORT = 5080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
START_MESSAGE = ""
BUFFER_SIZE = 1024
TIME_TO_WAIT = 10
score_dict = {}
final_text = ""

def handle_client(conn, addr, teams, start_event, done_event):
    """"
    :param
    conn -> TCP connection
    addr -> address
    teams -> teams to play
    start_event -> All Threads wait to the server to start the game
    done_event -> All Threads wait to the server to finish the game
    """
    try:

        name = conn.recv(BUFFER_SIZE).decode(FORMAT)

        print(f"[{addr}] {name}")
        teams[addr] = name
        global score_dict
        score_dict[addr] = 0

        start_event.wait()
        conn.send(START_MESSAGE)

        now = time.time()
        future = now + TIME_TO_WAIT

        while 1:
            try:
                conn.settimeout(future-time.time())
                data = conn.recv(BUFFER_SIZE).decode(FORMAT)
                score_dict[addr] += 1
            except:
                break
        done_event.wait()
        conn.send(final_text.encode(FORMAT))
        conn.close()
    except ConnectionResetError:
        print("client ", addr, "disconnected...")


def startAllServers():
    """"
    servers run tcp and udp simultaneously
    """
    print(f"This is TCP Server started, IP and Port {ADDR}")
    while 1:
        t_tcp = Thread(target=start_TCP_server)
        t_udp = Thread(target=start_UDP_server)

        t_udp.start()
        t_tcp.start()

        t_udp.join()
        t_tcp.join()

def start_TCP_server():
    """"
    Server creates new THREAD for each connection
    Ten seconds later,send welcome message and starts the game
    """
    teams = {}
    all_clients = []
    global score_dict
    score_dict = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    server.settimeout(TIME_TO_WAIT)

    start_game_event = threading.Event()
    done_game_event = threading.Event()

    while 1:
        try:
            conn, addr = server.accept()
            all_clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr, teams, start_game_event, done_game_event))
            thread.start()
            print(f"\n[ACTIVE CONNECTIONS] {len(all_clients)}")
        except:
            print("done waiting for client")
            break

    one_group, two_group = divide_to_groups(all_teams=teams)

    # Creating Welcome message
    welcome_msg = create_welcome_message(one_group, two_group)
    global START_MESSAGE
    START_MESSAGE = welcome_msg.encode(FORMAT)  # inform everyone that this is the welcome message

    if len(all_clients) == 0:
        print("no one came ...")
        return

    print("GAME START !!!!!!")
    start_game_event.set()  # Every Thread can send the Welcome message right now, and everybody can play

    time.sleep(TIME_TO_WAIT)
    global final_text
    final_text = calculate_game(one_group, two_group)  # Calculating the score game
    done_game_event.set()

    print("Game over, sending out offer requests...")


def calculate_game(group_a, group_b):
    """"
    calculating the scores from the game and return the results
    """
    sumA = 0
    sumB = 0
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
                    " characters.\n" + "Group" + winner + " wins!\n\nCongratulations to the winners\n==\n"

    for w in list_winner:
        text_to_print += w + "\n"
    return text_to_print


def divide_to_groups(all_teams):
    """
    dividing the teams into two groups
    """
    data = []
    for address in all_teams:
        data.append((address, all_teams[address]))

    random.shuffle(data)
    half_num_of_teams = int(len(all_teams)/2)

    one_group = data[:half_num_of_teams]
    two_group = data[half_num_of_teams:]

    return one_group, two_group

def create_welcome_message(one_group, two_group):
    """"
    creating and return the welcome message
    """

    welcome_msg = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n"
    for g in one_group:
        welcome_msg = welcome_msg + g[1] + "\n"
    welcome_msg += "Group 2:\n==\n"
    for g in two_group:
        welcome_msg = welcome_msg + g[1] + "\n"
    welcome_msg += "\nStart pressing keys on your keyboard as fast as you can!!\n"
    return welcome_msg
