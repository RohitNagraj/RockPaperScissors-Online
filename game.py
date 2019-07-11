class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def player(self, player, move):
        self.moves[player] = move

        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

            