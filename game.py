class Game:

    """
    Holds the game state and associated functions. Every game has 2 players.
    """

    def __init__(self, id):

        self.p1Went = False          # Whether p1 left
        self.p2Went = False          # Whether p2 left
        self.ready = False           # Are both the players ready
        self.id = id                 # Game instance ID
        self.moves = [None, None]    # Moves made by player 1 and 2 as strings
        self.wins = [0, 0]           # Count no. of wins
        self.ties = 0                # Count no. of ties

    def get_player_move(self, p):
        """
        :param p: [0,1] the player who's move is requested for
        :return: The move of player p
        """
        return self.moves[p]

    def play(self, player, move):
        """
        Makes a move
        :param player: [0, 1] player who's move is made
        :param move: ['Rock', 'Paper', 'Scissors']
        :return: None
        """
        self.moves[player] = move

        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        """
        :return: If the connection is established or not
        """
        return self.ready

    def both_went(self):
        """
        :return: whether both players left the game or not
        """
        return self.p1Went and self.p2Went

    def winner(self):
        """
        Determines which player won the game
        Assumes both players have made their moves

        -1 : Tie
         0 : Player 1 wins
         1 : Player 2 wins

        :return: player that won the game
        """
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1

        if p1 == "P" and p2 == "R":
            winner = 0

        elif p1 == "P" and p2 == "S":
            winner = 1

        elif p1 == "R" and p2 == "P":
            winner = 1

        elif p1 == "R" and p2 == "S":
            winner = 0

        elif p1 == "S" and p2 == "P":
            winner = 0

        elif p1 == "S" and p2 == "R":
            winner = 1

        return winner

    def reset_went(self):
        """
        Reset both the went booleans
        :return: None
        """
        self.p1Went = False
        self.p2Went = False
