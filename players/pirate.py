import pygame

from players.player import Player

class Pirate(Player):

    def __init__(self, x, y, pygame):
        super().__init__(x, y, 64, 40, 5, pygame.image.load("src/character1.png").convert_alpha())
        self._under_water = False
        self._air = 11
        self._air_count = 0

    def hit_box(self, zoom):
        return pygame.Rect(self._x + (20 * zoom), self._y+(20*zoom), 25 * zoom, 2)

    def hit_box_y(self, zoom):
        return pygame.Rect(self._x + (20 * zoom), self._y+(2*zoom), 25 * zoom, 28 * zoom)

    def complete_hit_box_y(self, zoom):
        return pygame.Rect(self._x + (20 * zoom), self._y+(20*zoom), 25 * zoom, 2 * zoom)

    def action(self):
        pass