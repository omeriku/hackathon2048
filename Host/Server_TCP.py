# from socket import *
#
# serverPort = 47980
# serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.bind(("", serverPort))
# serverSocket.listen(1)
# print("The server is ready to receive")
#
# while 1:
#     connectionSocket, addr = serverSocket.accept()
#
#     sentence = connectionSocket.recv(1024)
#     capitalizedSentence = sentence.upper()
#     connectionSocket.send(capitalizedSentence)
#     connectionSocket.close()


import socket
import threading
import time

# HEADER = 64
PORT = 47980
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.") #Todo delete prints

    connected = True
    while connected:
        msg_length = conn.recv(1024).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()


def start_TCP_server():
    server.listen()
    print(f"This is TCP Server started, IP and Port {ADDR}")

    now = time.time()
    future = now + 30 #Todo lower to 10
    while time.time() < future:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


# start_TCP_server()
