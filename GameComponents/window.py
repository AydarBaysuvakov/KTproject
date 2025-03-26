import pygame
import sys
from .algorithm import *
from .objects import *

FPS = 60
TITLE = 'Лабиринт'
SIZE = WIDTH, HEIGHT = 600, 600
MAP = ROWS, COLS = 20, 20

def terminate():
    pygame.quit()
    sys.exit()

class Window:
    def __init__(self, screen, size=SIZE, background=None, coords=(0, 0)):
        self.set_screen(screen, size, background, coords)

    def set_screen(self, screen, size=SIZE, background=None, coords=(0, 0)):
        self.screen = screen
        self.coords = coords
        self.size = size
        if background is None:
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill(pygame.color.Color('black'))
        #elif background[0] == 'Image':
        #    self.background = pygame.transform.scale(load_image(background_fn[1]), size)
        elif background[0] == 'Color':
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill(pygame.color.Color(background[1]))
        self.screen.blit(self.background, coords)

    def show(self):
        clock = pygame.time.Clock()
        run = True
        last_event = None
        while run:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()
        
class GameWindow(Window):
    def __init__(self, screen, game):
        super().__init__(screen)
        self.new_level()
        self.game = game

    def new_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.camera = Camera()
        self.generate_level()

    def show(self):
        clock = pygame.time.Clock()
        run = True
        events = {}
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    events[event.key] = True
                    if event.key == pygame.K_ESCAPE:
                        return 'back'
                    if event.key == pygame.K_KP_0:
                        return 'restart'
                if event.type == pygame.KEYUP:
                    events[event.key] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    events[event.button] = True
                if event.type == pygame.MOUSEBUTTONUP:
                    events[event.button] = False
            self.player.get_event(events)
            if self.player.event == 'restart':
                return 'restart'
            self.draw()
            clock.tick(FPS)
        pygame.quit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.camera.update(self.player)
        for sprite in self.all_sprites:
            self.camera.apply(sprite)
        pygame.display.flip()

    def generate_level(self):
        self.ver, self.hor, self.start, self.finish = create_labirint(*MAP)
        self.Spawn_Cup()
        self.Spawn_Wall()
        self.Spawn_Player()


    def Spawn_Player(self):
        self.player = Player(self.all_sprites, (45 * self.start[0] + 5, 45 * self.start[1] + 5), self)
    
    def Spawn_Cup(self):
        Cup(self.all_sprites, (45 * self.finish[0] + 5, 45 * self.finish[1] + 5))

    def Spawn_Wall(self):
        for i in range(ROWS):
            Wall([self.all_sprites, self.walls], (-5, 45 * i), 1)
            for j in range(COLS):
                if (self.ver[i][j + 1]):
                    Wall([self.all_sprites, self.walls], (45 * j + 40, 45 * i), 1)
                if (self.hor[i + 1][j]):
                    Wall([self.all_sprites, self.walls], (45 * j, 45 * i + 40), 0)
        for j in range(COLS):
            Wall([self.all_sprites, self.walls], (45 * j, -5), 0)
        
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)