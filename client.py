import pygame

from network import Network

pygame.font.init()

disconnected = False

# Window width and height
width = 500
height = 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    """
    To create and interface a button in pygame
    """
    def __init__(self, text, x, y, color):
        """
        :param text: Text to write in the button
        :param x: width of button
        :param y: height of button
        :param color: color of button
        """
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 120
        self.height = 50

    def draw(self, win):
        """
        Draws the button on the pygame window passed as param
        :param win: pygame window
        :return: None
        """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, 1, (255, 255, 255))

        x = (self.x + round(self.width/2) - round(text.get_width()/2))
        y = (self.y + round(self.height/2) - round(text.get_height()/2))
        win.blit(text, (x, y))

    def click(self, pos):
        """
        Determines of the button is clicked
        :param pos: coordinates of mouse click
        :return: True if clicked, False otherwise
        """
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_window(win, game, p):
    """
    Updates the whole pygame window
    :param win: pygame window instance
    :param game: current game object that determines the game state
    :param p: [0, 1] player no.
    :return: None
    """
    win.fill((255, 255, 255))

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Waiting for player...", 1, (180, 0, 255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    else:
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("You", 1, (180, 0, 255))
        win.blit(text, (80, 50))

        text = font.render("Opponent", 1, (180, 0, 255))
        win.blit(text, (280, 50))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_went():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))

        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (80, 170))
            win.blit(text1, (280, 170))
        else:
            win.blit(text1, (80, 170))
            win.blit(text2, (280, 170))

        for btn in btns:
            btn.draw(win)
    pygame.display.update()


black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
btns = [Button("Rock", 40, 300, black), Button("Scissors", 190, 300, red), Button("Paper", 340, 300, blue)]


def main_game():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_p())
    print("You are player: ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.both_went():
            redraw_window(win, game, player)
            pygame.time.delay(200)
            try:
                game = n.send("reset")
            except TypeError as e:
                run = False
                print("Couldn't get game", e)
                break

            font = pygame.font.SysFont("comicsans", 70)

            if game.winner() == player:
                text = font.render("You won!", 1, (0, 150, 0))
            elif game.winner() == -1:
                text = font.render("Draw", 1, (80, 80, 80))
            else:
                text = font.render("You Lost!", 1, (255, 0, 0))

            win.blit(text, ((width/2-text.get_width()/2), (height/2 - text.get_height()/2)))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0 and not game.p1Went:
                            n.send(btn.text)
                        elif player == 1 and not game.p2Went:
                            n.send(btn.text)

        redraw_window(win, game, player)





def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((255, 255, 255))
        font = pygame.font.SysFont('comicsans', 60)
        if disconnected:
            text = font.render("Opponent disconnected!", 1, (0, 80, 255))
            win.blit(text, (30, 230))

        text = font.render("Click to connect!", 1, (0, 80, 255))
        win.blit(text, (80, 230))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                main_game()




if __name__ == '__main__':
    global disconnected

    while True:
        menu_screen()
        disconnected = True
