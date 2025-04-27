import pygame
from .image import load_image

class Object(pygame.sprite.Sprite):
    def __init__(self, group, image_name=None, size=(10, 10), colorkey=None, form='rect'):
        super().__init__(group)
        self.load_image(image_name, size, colorkey, form)
        
        self.image = self.image_src.copy()
        self.rect = self.image.get_rect()
        self.rect.w, self.rect.h = size
        self.mask = pygame.mask.from_surface(self.image)

    def load_image(self, image_name, size, colorkey, form):
        if image_name is None:
            self.image_src = pygame.Surface(size)
            self.image_src.fill(pygame.color.Color('white'))
        elif image_name[0] == 'Image':
            self.image_src = load_image(image_name[1], colorkey=colorkey)
            self.image_src = pygame.transform.scale(self.image_src, size)
        elif image_name[0] == 'Color':
            self.image_src = pygame.Surface(size)
            if form == 'circle':
                pygame.draw.circle(self.image_src, pygame.Color(image_name[1]),
                                   (size[0] // 2, size[1] // 2), size[0] // 2)
                self.image_src.set_colorkey(pygame.color.Color('black'))
            else:
                self.image_src.fill(pygame.color.Color(image_name[1]))
                
class Wall(Object):
    def __init__(self, group, pos, type):
        size = [5, 40] if type else [40, 5]
        super().__init__(group[0], ('Color', 'red'), size=size)
        self.add(group[1])
        self.rect.left, self.rect.top = pos
        
class Door(Object):
    def __init__(self, group, pos, type, button_index):
        size = [5, 40] if type else [40, 5]
        super().__init__(group[0], ('Color', 'blue'), size=size)
        self.add(group[1])
        self.rect.left, self.rect.top = pos
        self.button_index = button_index

class Button(Object):
    def __init__(self, group, pos, index):
        super().__init__(group, ('Color', 'blue'), size=[30, 30], form='circle')
        self.rect.left, self.rect.top = pos
        self.index = index
        
class Cup(Object):
    def __init__(self, group, pos):
        super().__init__(group, ('Color', 'yellow'), size=[30, 30], form='circle')
        self.rect.left, self.rect.top = pos
                
class Player(Object):
    Vx, Vy = 0, 0
    event = None
    event_value = 0

    def __init__(self, group, pos, window):
        super().__init__(group, ('Color', 'white'), size=[30, 30], form='circle')
        self.rect.left, self.rect.top = pos
        self.window = window

    def get_event(self, events):
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
                
        if pygame.sprite.spritecollideany(self, [self.window.cup]):
            self.event = 'win'
        for button in self.window.buttons:
            if pygame.sprite.spritecollideany(self, [button]):
                self.event = 'button'
                print('collide', button.index)
                self.event_value = button