import pygame
from typing import overload, Union


class Item:
    @overload
    def __init__(self, x: int, y: int, type: int):
        ...

    @overload
    def __init__(self, pos: tuple[int, int], type: int):
        ...

    def __init__(self, x_or_pos: Union[int, tuple[int, int]], y_or_type: int, maybe_type: int = None):
        if maybe_type is not None:
            self._x = x_or_pos
            self._y = y_or_type
            self._type = maybe_type
        else:
            self._x = x_or_pos[0]
            self._y = x_or_pos[1]
            self._type = y_or_type

        self._dy = None
        self._px = 0
        self._quant_frames = None
        self._dx = None
        self._img = None
        self._timer = 0
        self._delay = 10
        self.init_img(self._type)

    def update(self):
        self._timer += 1
        if self._timer >= self._delay:
            self._timer = 0
            self._px += self._dx
            if self._px >= self._quant_frames * self._dx:
                self._px = 0

    def draw(self, screen, zoom):
        frame_rect = pygame.Rect(self._px, 0, self._dx, self._dy)
        frame = self._img.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (self._dx * zoom, self._dy * zoom))
        screen.blit(scaled_frame, (self._x, self._y))

    def add_x(self, x):
        self._x += x

    def add_y(self, y):
        self._y += y

    def init_img(self, type):
        if type == 1:
            self._img = pygame.image.load("src/coin.png").convert_alpha()
            self._dx = 16
            self._dy = 16
            self._quant_frames = 4
        elif type == 2:
            self._img = pygame.image.load("src/map.png").convert_alpha()
            self._dx = 20
            self._dy = 20
            self._quant_frames = 7

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_type(self):
        return self._type
