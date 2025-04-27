from .window import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(TITLE)
        self.window = GameWindow(self.screen)
        self.start()

    def start(self):
        self.window.show()