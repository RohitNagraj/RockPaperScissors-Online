import _thread
import pickle
import socket

from game import Game

server = "192.168.0.102"    # Local IP address of the server
port = 5555                 # Port to listen

# Instantiate server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Setup server
try:
    s.bind((server, port))
except socket.error as e:
    print(e)

# Start server
s.listen(2)
print("Server started, waiting for connection...")


connected = set()    # Holds the IDs of connected players
games = {}           # gameId: Game instance
idCount = 0          # Holds the count of connected players


def threaded_client(conn, p, gameId):
    """
    A new instance of this client is created for every new client that connects.
    All the instances run on their own thread.
    This implements all the server side functionality for the client
    :param conn: socket connection instance
    :param p: [0, 1] player number
    :param gameId: to which game the player belongs
    :return: None
    """
    global idCount

    # As soon as the player is connected, his player number is send as encoded string
    conn.send(str.encode(str(p)))

    reply = ""

    while True:

        # Data from client is an encoded string as defined in Network
        data = conn.recv(4096).decode()

        try:
            # if the game exists, fetch its instance
            if gameId in games:
                game = games[gameId]

                if not data:
                    break

                # if we have data
                else:
                    if data == 'reset':
                        game.reset()

                    # if it is a move, 'rock', 'paper' or 'scissors'
                    elif data != 'get':
                        game.play(p, data)

                    # Any required operations are done and the whole game instance is sent
                    reply = game
                    conn.send(pickle.dumps(reply))

            else:
                break

        except socket.error as e:
            print(e)
            break

    print("Lost connection")

    # If the game still exists
    try:
        del games[gameId]
        print("Closing game: ", gameId)

    except KeyError as e:
        print(e)

    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to", addr)

    # Increment player count
    idCount += 1
    # Assume player 1
    p = 0
    # Game ID is int division of idCount
    gameId = (idCount - 1) // 2

    # If he's 1st player, create a new game with gameId
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating new game")

    # Else, ready the game with gameId and make that player player 2
    else:
        games[gameId].ready = True
        p = 1

    # Start the player's thread
    _thread.start_new_thread(threaded_client, (conn, p, gameId))
