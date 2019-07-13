import pickle
import socket


class Network:
    """
    Interfaces the socket server for the client
    """
    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.102"    # Local IP address of the server
        self.port = 5555                 # Port on which the server is running
        self.addr = (self.server, self.port)
        try:
            self.p = self.connect()          # Player number
        except socket.error as e:
            print(e)

    def get_p(self):
        """
        :return: [0, 1] player number
        """
        return self.p

    def connect(self):
        """
        Connects the new client to the server
        :return: The player number assigned by the server
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        """
        Send data from client to server and receive data from server
        Data from client to server is encoded string
        Data from server to client is pickle object
        :param data: (string) data to send
        :return: (game instance) updated game instance
        """
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
