import pygame
import sys
from .labirint import *
from .objects import *
from .bot import *

FPS = 60
TITLE = 'Лабиринт'
SIZE = WIDTH, HEIGHT = 1280, 720
MAP = COLS, ROWS = 6, 6
BOT = True
SMOKE = False
EXPLOSIONS = False
EXPLOSION_FREQ = 600
MOVE_FREQ = 30
WARNING_TIME = EXPLOSION_FREQ // 6
EXPLOSION_TIME = WARNING_TIME // 2
EXPLOSION_COUNT = COLS * ROWS * 3 // 4
GAME_END_EVENTS = ['restart', 'win', 'boom']

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
        super().__init__(screen, background=['Image', 'cosmos1.png'])
        self.new_level()

    def new_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls       = pygame.sprite.Group()
        self.smoke       = pygame.sprite.Group()
        self.warnings    = pygame.sprite.Group()
        self.explosions  = pygame.sprite.Group()
        self.doors       = []
        self.buttons     = []
        self.camera      = Camera()
        self.zero        = Dummy(self.all_sprites)
        self.generate_level()

    def show(self):
        clock = pygame.time.Clock()
        time_0 = pygame.time.get_ticks()
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
            if self.player.event in GAME_END_EVENTS:
                return self.player.event
            if self.player.event == 'button':
                self.open_door()
            self.draw()
            clock.tick(FPS)
            cycle = (pygame.time.get_ticks() - time_0) // 16
            if EXPLOSIONS:
                if cycle % EXPLOSION_FREQ == 0:
                    self.Spawn_Explosion()
                elif cycle % EXPLOSION_FREQ == WARNING_TIME:
                    self.explosion()
                elif cycle % EXPLOSION_FREQ == EXPLOSION_TIME + WARNING_TIME:
                    self.clear_explosion()
            if BOT:
                if cycle % MOVE_FREQ == 0:
                    cell = self.path[self.index]
                    player_pos = self.player.rect
                    zero_pos = self.zero.rect
                    x, y = player_pos.left - zero_pos.left, player_pos.top - zero_pos.top
                    dx, dy = x - cell[0] * 54 - 58, y - cell[1] * 54 - 58
                    self.player.rect.left -= dx
                    self.player.rect.top  -= dy
                    self.index += 1
        pygame.quit()

    def draw(self):
        self.screen.blit(self.background, self.coords)
        self.all_sprites.draw(self.screen)
        self.camera.update(self.player)
        for sprite in self.all_sprites:
            self.camera.apply(sprite)
        pygame.display.flip()

    def generate_level(self):
        self.labirint = Labirint(*MAP).get_labirint()
        while not self.check():
            self.labirint = Labirint(*MAP).get_labirint()
        self.path = []
        for i in self.way:
            if type(i) == list:
                self.path.extend(i)
        print(self.path)
        self.index = 0
        self.Spawn_Portal()
        self.Spawn_Wall()
        self.Spawn_Player()
        self.Spawn_Door()
        if SMOKE:
            self.Spawn_Smoke()
            
    def check(self):
        self.way = Bot(self.labirint).get_way()
        if False in self.way or not self.way or len(self.way) != (Labirint.doors + 1) * 2:
            return False
        return True

    def Spawn_Player(self):
        self.player = Player(self.all_sprites, (54 * self.labirint['start'][0] + 58, 54 * self.labirint['start'][1] + 58), self)
    
    def Spawn_Portal(self):
        self.portal = Portal(self.all_sprites, (54 * self.labirint['finish'][0] + 58, 54 * self.labirint['finish'][1] + 58))

    def Spawn_Wall(self):
        for i in range(ROWS + 1):
            for j in range(COLS + 1):
                if (self.labirint['verticals'][i][j]):
                    Wall([self.all_sprites, self.walls], (54 * j + 48, 54 * i), 1)
                if (self.labirint['horizonts'][i][j]):
                    Wall([self.all_sprites, self.walls], (54 * j, 54 * i + 48), 0)
    
    def Spawn_Door(self):
        for door in self.labirint['doors']:
            if door[0] == 'verticals':
                self.doors.append(Door([self.all_sprites, self.walls], (54 * door[1][1] + 48, 54 * door[1][0]), 1, door[2]))
            if door[0] == 'horizonts':
                self.doors.append(Door([self.all_sprites, self.walls], (54 * door[1][1], 54 * door[1][0] + 48), 0, door[2]))
                
        for button in self.labirint['buttons']:
                self.buttons.append(Button(self.all_sprites, (54 * button[0] + 60, 54 * button[1] + 60), button[2]))
        
    def open_door(self):
        for i, door in enumerate(self.doors):
            if door.button_index == self.player.event_value.index:
                door.kill()
                self.doors.pop(i)
        for i, btn in enumerate(self.buttons):
            if btn.index == self.player.event_value.index:
                btn.kill()
                self.buttons.pop(i)
                
    def Spawn_Smoke(self):
        for i in range(ROWS + 1):
            for j in range(COLS + 1):
                Smoke([self.all_sprites, self.smoke], (54 * j, 54 * i))
            
    def Spawn_Explosion(self):
        dx, dy = self.zero.rect.x, self.zero.rect.y
        for i in range(EXPLOSION_COUNT):
            x, y = (randint(0, COLS - 1), randint(0, ROWS - 1))
            Warning([self.all_sprites, self.warnings], (54 * x + 60 + dx, 54 * y + 60 + dy))
    
    def explosion(self):
        for warning in self.warnings:
            Explosion([self.all_sprites, self.explosions], (warning.rect.x, warning.rect.y))
            warning.kill()
    
    def clear_explosion(self):
        for explosion in self.explosions:
            explosion.kill()
    
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