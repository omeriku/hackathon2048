import random
import time
import socket



# def startGame(a_group, b_group, all_clients, server):
#     FORMAT = 'utf-8'
#     now = time.time()
#     future = now + 10
#     score = {}
#     for g in a_group:
#         score[g[0]] = 0
#     for g in b_group:
#         score[g[0]] = 0
#     print("TYPE !!!!!!")
#     # print("server is ", server)
#     while time.time() < future:
#         data = server.recv(1024).decode(FORMAT)
#         # print("ADDRESS :" , address)
#         print("DATA: ", data)
#         # try:
#         #     score[address] += 1
#         # except:
#         #     print("cannot save data from :", address)
#         #     continue
#     message = "gameOver"
#     for client in all_clients:
#         client.send(message)
#     print("Score:", score)

