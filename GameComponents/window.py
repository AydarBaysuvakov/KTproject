import pygame
import sys
from .labirint import *
from .objects import *

FPS = 60
TITLE = 'Лабиринт'
SIZE = WIDTH, HEIGHT = 700, 700
MAP = COLS, ROWS = 15, 10

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
        elif background[0] == 'Image':
            self.background = pygame.transform.scale(load_image(background[1]), size)
        elif background[0] == 'Color':
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill(pygame.color.Color(background[1]))
        self.screen.blit(self.background, self.coords)

    def show(self):
        clock = pygame.time.Clock()
        run = True
        last_event = None
        while run:
            self.screen.blit(self.background, self.coords)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()
        return last_event
        
class GameWindow(Window):
    def __init__(self, screen):
        super().__init__(screen)
        self.new_level()

    def new_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.doors = []
        self.buttons = []
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
            if self.player.event == 'win':
                print('win')
                return 'win'
            if self.player.event == 'button':
                self.open_door()
            self.draw()
            clock.tick(FPS)
        pygame.quit()

    def draw(self):
        self.screen.blit(self.background, self.coords)
        self.all_sprites.draw(self.screen)
        self.camera.update(self.player)
        for sprite in self.all_sprites:
            self.camera.apply(sprite)
        pygame.display.flip()

    def generate_level(self):
        self.labirint = create_labirint(*MAP)
        self.Spawn_Cup()
        self.Spawn_Wall()
        self.Spawn_Player()
        self.Spawn_Door()

    def Spawn_Player(self):
        self.player = Player(self.all_sprites, (45 * self.labirint['start'][0] + 50, 45 * self.labirint['start'][1] + 50), self)
    
    def Spawn_Cup(self):
        self.cup    = Cup(self.all_sprites, (45 * self.labirint['finish'][0] + 50, 45 * self.labirint['finish'][1] + 50))

    def Spawn_Wall(self):
        for i in range(ROWS + 1):
            for j in range(COLS + 1):
                if (self.labirint['verticals'][i][j]):
                    Wall([self.all_sprites, self.walls], (45 * j + 40, 45 * i), 1)
                if (self.labirint['horizonts'][i][j]):
                    Wall([self.all_sprites, self.walls], (45 * j, 45 * i + 40), 0)
    
    def Spawn_Door(self):
        for door in self.labirint['doors']:
            if door[0] == 'verticals':
                self.doors.append(Door([self.all_sprites, self.walls], (45 * door[1][1] + 40, 45 * door[1][0]), 1, door[2]))
            if door[0] == 'horizonts':
                self.doors.append(Door([self.all_sprites, self.walls], (45 * door[1][1], 45 * door[1][0] + 40), 0, door[2]))
                
        for button in self.labirint['buttons']:
                self.buttons.append(Button(self.all_sprites, (45 * button[0] + 50, 45 * button[1] + 50), button[2]))
        
    def open_door(self):
        for i, door in enumerate(self.doors):
            if door.button_index == self.player.event_value.index:
                door.kill()
                self.doors.pop(i)
        for i, btn in enumerate(self.buttons):
            if btn.index == self.player.event_value.index:
                btn.kill()
                self.buttons.pop(i)
    
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