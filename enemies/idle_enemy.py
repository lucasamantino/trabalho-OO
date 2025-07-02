import pygame

class IdleEnemy:
    def __init__(self, x, y, type, dir):
        self._x = x
        self._y = y
        self._dy = None
        self._px = 0
        self._py = 0
        self._dir = dir
        self._quant_frames = None
        self._dx = None
        self._img = None
        self._timer = 0
        self._delay = 10
        self.init_img(type)
        self._type = type
        self._attack = True
        self._attack_delay = 0

    def update(self):
        self._py = 0

        if self._attack_delay > 0:
            self._attack_delay -= 1

        if self._attack and self._attack_delay <= 0:
            self._py = self._dy
            self._timer += 1
            if self._timer >= self._delay:
                self._timer = 0
                self._px += self._dx
                if self._px >= self._quant_frames * self._dx:
                    self._px = 0
                    self._attack_delay = 50
                    return True
        return False

    def draw(self, screen, zoom):
        # Da zoom
        frame_rect = pygame.Rect(self._px, self._py, self._dx, self._dy)
        frame = self._img.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (self._dx * zoom, self._dy * zoom))
        if self._dir == 1:
            scaled_frame = pygame.transform.flip(scaled_frame, True, False)
        # desenha
        screen.blit(scaled_frame, (self._x, self._y))

    def init_img(self, type):
        if type == 1:
            self._img = pygame.image.load("src/cannon.png").convert_alpha()
            self._dx = 40
            self._dy = 26
            self._quant_frames = 7
        if type == 2:
            self._img = pygame.image.load("src/seashell.png").convert_alpha()
            self._dx = 48
            self._dy = 38
            self._quant_frames = 5


    def add_x(self, x):
        self._x += x

    def add_y(self, y):
        self._y += y


    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_dir(self):
        return self._dir

    def get_type(self):
        return self._type
