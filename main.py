from Host.Server_TCP import startGame
from threading import Thread
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Thread(target=startGame).start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
