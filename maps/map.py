import json
import pygame

class Map:
    def __init__(self, num, zoom):
        self.zoom = zoom
        self.__px = 0
        self.__py = 0

        # carrega aa imagens do mapa
        original = pygame.image.load(f'maps/data/map{num}.png').convert_alpha()
        w = int(original.get_width() * zoom)
        h = int(original.get_height() * zoom)
        self.background = pygame.transform.scale(original, (w, h))

        original = pygame.image.load(f'maps/data/map{num}-top.png').convert_alpha()
        w = int(original.get_width() * zoom)
        h = int(original.get_height() * zoom)
        self.background_top = pygame.transform.scale(original, (w, h))

        with open(f'maps/data/map{num}.json', 'r') as arquivo:
            dados = json.load(arquivo)
        self.tiles = dados['map']
        self.water = dados['water']
        self.coins = dados['coins']
        self.treasures = dados['treasures']
        self.enemies = dados['enemies']
        self.width = dados['width']
        self.height = dados['height']

    def draw(self, screen):
        screen.blit(self.background, (self.__px, self.__py))

    def draw_top(self, screen):
        screen.blit(self.background_top, (self.__px, self.__py))

    def get_tiles(self):
        return self.tiles

    def get_treasures(self):
        return self.treasures

    def get_water(self):
        return self.water

    def get_enemies(self):
        return self.enemies

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def sety(self, y):
        self.__py = y

    def get_coins(self):
        return self.coins

    def get_x(self):
        return self.__px

    def get_y(self):
        return self.__py

    def addx(self, speed):
        self.__px += speed

    def addy(self, speed):
        self.__py += speed
