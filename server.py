import _thread
import pickle
import socket

from game import Game

server = "192.168.0.102"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Server started, waiting for connection...")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameID):
    pass


while True:
    conn, addr = s.accept()
    print("Connected to", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2:
        games[gameId] = Game(gameId)
        print("Creating new game")

    else:
        games[gameId].ready = True
        p = 1

    _thread.start_new_thread(threaded_client, (conn,))
