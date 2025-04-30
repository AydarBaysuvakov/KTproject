import pygame
from .image import load_image

ANIM_FREQ = 5
smoke_src = pygame.image.load('Data/smoke.png')

class Object(pygame.sprite.Sprite):
    def __init__(self, group, image_name=None, size=(10, 10), colorkey=None, form='rect'):
        super().__init__(group)
        self.load_image(image_name, size, colorkey, form)
        
        self.image = self.image_src[0].copy()
        self.image_index = 0
        self.image_count = len(self.image_src)
        self.rect = self.image.get_rect()
        self.rect.w, self.rect.h = size
        self.mask = pygame.mask.from_surface(self.image)

    def load_image(self, image_name, size, colorkey, form):
        self.image_src = []
        if image_name is None:
            self.image_src.append(pygame.Surface(size))
            self.image_src[0].fill(pygame.color.Color('white'))
        elif image_name[0] == 'Image':
            for image in image_name[1:]:
                image_src = load_image(image, colorkey=colorkey)
                image_src = pygame.transform.scale(image_src, size)
                self.image_src.append(image_src)
        elif image_name[0] == 'Src':
            for image in image_name[1:]:
                image_src = image.convert_alpha()
                image_src = pygame.transform.scale(image_src, size)
                self.image_src.append(image_src)
        elif image_name[0] == 'Color':
            self.image_src.append(pygame.Surface(size))
            if form == 'circle':
                pygame.draw.circle(self.image_src[0], pygame.Color(image_name[1]),
                                   (size[0] // 2, size[1] // 2), size[0] // 2)
                self.image_src[0].set_colorkey(pygame.color.Color('black'))
            else:
                self.image_src[0].fill(pygame.color.Color(image_name[1]))
                
class Wall(Object):
    def __init__(self, group, pos, type):
        size = [6, 48] if type else [48, 6]
        super().__init__(group[0], ('Color', '#a62307'), size=size)
        self.add(group[1])
        self.rect.left, self.rect.top = pos
        
class Door(Object):
    def __init__(self, group, pos, type, button_index):
        size = [6, 48] if type else [48, 6]
        super().__init__(group[0], ('Color', '#aa870e'), size=size)
        self.add(group[1])
        self.rect.left, self.rect.top = pos
        self.button_index = button_index

class Button(Object):
    def __init__(self, group, pos, index):
        super().__init__(group, ('Image', 'card.png'), size=[36, 24], form='circle')
        self.rect.left, self.rect.top = pos
        self.index = index

class Smoke(Object):
    def __init__(self, group, pos):
        super().__init__(group, ('Src', smoke_src), size=[75, 75], form='circle')
        self.rect.left, self.rect.top = pos
        
class Warning(Object):
    def __init__(self, group, pos):
        super().__init__(group, ('Color', 'orange'), size=[42, 42], form='circle')
        self.rect.left, self.rect.top = pos
        
class Explosion(Object):
    def __init__(self, group, pos):
        super().__init__(group, ('Color', 'red'), size=[42, 42], form='circle')
        self.rect.left, self.rect.top = pos
        
class Portal(Object):
    def __init__(self, group, pos):
        super().__init__(group, ('Image', 'portal4.png'), size=[42, 42], form='circle')
        self.rect.left, self.rect.top = pos

class Dummy(Object):
    def __init__(self, group):
        super().__init__(group, ('Color', 'white'), size=[2, 2], form='circle')
        self.rect.left, self.rect.top = (0, 0)
                
class Player(Object):
    Vx, Vy = 0, 0
    event = None
    event_value = 0

    def __init__(self, group, pos, window):
        super().__init__(group, ('Image', 'ufo_idle.png', 'ufo_beam1.png', 'ufo_beam2.png'), size=[45, 30], form='circle')
        self.rect.left, self.rect.top = pos
        self.window = window

    def get_event(self, events):
        self.image_index = (self.image_index + 1) % (self.image_count * ANIM_FREQ)
        self.image = self.image_src[self.image_index // ANIM_FREQ].copy()
        
        for key, value in events.items():
            if key == pygame.K_UP and value:
                self.Vy = -4
            if key == pygame.K_DOWN and value:
                self.Vy = 4
            if key == pygame.K_RIGHT and value:
                self.Vx = 4
            if key == pygame.K_LEFT and value:
                self.Vx = -4
                
        if (pygame.K_UP in events and not events[pygame.K_UP]) and (pygame.K_DOWN not in events):
            self.Vy = 0
        if (pygame.K_UP not in events) and (pygame.K_DOWN in events and not events[pygame.K_DOWN]):
            self.Vy = 0
        if (pygame.K_UP in events and not events[pygame.K_UP]) and (pygame.K_DOWN in events and not events[pygame.K_DOWN]):
            self.Vy = 0
        if (pygame.K_RIGHT in events and not events[pygame.K_RIGHT]) and (pygame.K_LEFT not in events):
            self.Vx = 0
        if (pygame.K_RIGHT not in events) and (pygame.K_LEFT in events and not events[pygame.K_LEFT]):
            self.Vx = 0
        if (pygame.K_RIGHT in events and not events[pygame.K_RIGHT]) and (pygame.K_LEFT in events and not events[pygame.K_LEFT]):
            self.Vx = 0
        #print(self.Vy)
            
        self.move()

    def move(self):
        mod_x, mod_y = int(abs(self.Vx)), int(abs(self.Vy))
        dir_x, dir_y = (self.Vx / mod_x) if mod_x else 0  , (self.Vy / mod_y) if mod_y else 0
        for i in range(mod_x):
            self.rect = self.rect.move(dir_x, 0)
            if pygame.sprite.spritecollideany(self, self.window.walls):
                self.rect = self.rect.move(-dir_x, 0)
        for i in range(mod_y):
            self.rect = self.rect.move(0, dir_y)
            if pygame.sprite.spritecollideany(self, self.window.walls):
                self.rect = self.rect.move(0, -dir_y)
                
        if pygame.sprite.spritecollideany(self, [self.window.portal]):
            self.event = 'win'
        if pygame.sprite.spritecollideany(self, self.window.explosions):
            print('boom')
            self.event = 'boom'
        
        for smoke in self.window.smoke:
            if pygame.sprite.spritecollideany(self, [smoke]):
                smoke.kill()
            
        for button in self.window.buttons:
            if pygame.sprite.spritecollideany(self, [button]):
                self.event = 'button'
                self.event_value = button