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
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        data = conn.recv(4096).decode()

        try:
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset()

                    elif data != 'get':
                        game.play(p, data)

                    reply = game
                    conn.send(pickle.dumps(reply))

            else:
                break
        except:
            break
    print("Lost connection")

    try:
        del games[gameId]
        print("Closing game: ", gameId)

    except:
        pass

    idCount -= 1
    conn.close()


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

    _thread.start_new_thread(threaded_client, (conn, p, gameId))
