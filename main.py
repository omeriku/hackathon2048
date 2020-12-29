from Player.Server_UDP import start_UDP_server
from Host.Server_TCP import start_TCP_server
from threading import Thread
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Thread(target=start_UDP_server).start()
    Thread(target=start_TCP_server).start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
