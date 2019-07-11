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


def threaded_client(conn, p, gameID):
    pass


while True:
    conn, addr = s.accept()
    print("Connected to", addr)
