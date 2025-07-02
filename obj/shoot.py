import pygame

class Shoot:

    def __init__(self, x, y, type, dir):
        self._x = x
        self._y = y
        self._dx = None
        self._img = None
        self.init_img(type)
        self._type = type
        self._dir = dir
        self._speed = 40

    def update(self):
        if self._dir == 0:
            self._x -= self._speed
        else:
            self._x += self._speed

    def draw(self, screen, zoom):
        #Da zoom
        frame_rect = pygame.Rect(0, 0, self._dx, self._dx)
        frame = self._img.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (self._dx * zoom, self._dx * zoom))

        #desenha
        screen.blit(scaled_frame, (self._x, self._y))

    def add_x(self, x):
        self._x += x

    def add_y(self, y):
        self._y += y

    def init_img(self, type):
        if type == 1:
            self._img = pygame.image.load("src/ball.png").convert_alpha()
            self._dx = 16
        if type == 2:
            self._img = pygame.image.load("src/pearl.png").convert_alpha()
            self._dx = 16


    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
