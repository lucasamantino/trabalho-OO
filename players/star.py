import pygame

from players.player import Player

class Star(Player):

    def __init__(self, x, y, pygame):
        super().__init__(x, y, 34, 30, 5, pygame.image.load("src/character2.png").convert_alpha())
        self._under_water = True
        self._air = 11
        self._air_count = 0

    def hit_box(self, zoom):
        return pygame.Rect(self._x + (3 * zoom), self._y+(4*zoom), 27 * zoom, 2)

    def hit_box_y(self, zoom):
        return pygame.Rect(self._x + (3 * zoom), self._y+(4*zoom), 27 * zoom, 25 * zoom)

    def complete_hit_box_y(self, zoom):
        return pygame.Rect(self._x + (20 * zoom), self._y+(20*zoom), 25 * zoom, 2 * zoom)

    def action(self):
        if self._attack:
            self._speed = 16
            if self._dir == 1:
                self._x += self._speed
            else:
                self._x -= self._speed
        else:
            self._speed = 8