import random
import time
import socket

def divide_to_groups(all_teams):
    one_group = []
    two_group = []
    all_teams = dict(all_teams)
    data = []
    for address in all_teams:
        data.append((address, all_teams[address]))

    random.shuffle(data)
    half_num_of_teams = int(len(all_teams)/2)

    one_group = data[:half_num_of_teams]
    two_group = data[half_num_of_teams:]

    return one_group, two_group


def startGame(a_group, b_group, all_clients, server):
    now = time.time()
    future = now + 10
    score = {}
    for g in a_group:
        score[g[0]] = 0
    for g in b_group:
        score[g[0]] = 0
    print("TYPE !!!!!!")

    while time.time() < future:
        try:
            data, address = server.recvfrom(1024)
            score[address] += 1
        except:continue
    message = "gameOver"
    for client in all_clients:
        client.send(message)
    print("Score:", score)

