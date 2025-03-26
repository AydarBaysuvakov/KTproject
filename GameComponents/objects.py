import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, group, image_name=None, size=(10, 10), take_size=False, colorkey=None, form='rect'):
        super().__init__(group)
        self.load_image(image_name, size, colorkey, form, take_size)
        self.image = self.image_src.copy()
        self.rect = self.image.get_rect()
        if take_size:
            self.rect.w = size[0]
            self.rect.h = size[1]
        self.mask = pygame.mask.from_surface(self.image)

    def load_image(self, image_name, size, colorkey, form, take_size):
        if image_name is None:
            self.image_src = pygame.Surface(size)
            self.image_src.fill(pygame.color.Color('white'))
        #elif image_name[0] == 'Image':
        #    self.image_src = load_image(image_name[1], colorkey=colorkey)
        #    if take_size:
        #        self.image_src = pygame.transform.scale(self.image_src, size)
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
        super().__init__(group[0], ('Color', 'red'), size=size, take_size=True)
        self.add(group[1])
        self.rect.left = pos[0]
        self.rect.top = pos[1]
        
class Cup(Object):
    def __init__(self, group, pos):
        super().__init__(group, ('Color', 'yellow'), size=[30, 30], take_size=True, form='circle')
        self.rect.left = pos[0]
        self.rect.top = pos[1]
                
class Player(Object):
    Vx, Vy = 0, 0
    event = None

    def __init__(self, group, pos, window, image_name=['Color', 'blue'], form='circle'):
        super().__init__(group, image_name, size=[30, 30], take_size=True)
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