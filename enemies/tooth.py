import pygame

class Tooth:
    def __init__(self, x, y):
        self._attack = False
        self._x = x
        self._y = y
        self._speed = 2
        self._range = 300
        self._img = pygame.image.load("src/tooth.png").convert_alpha()
        self._dx = 34
        self._dy = 30
        self._px = 0
        self._py = 0
        self._max_frames = 4
        self._animation_timer = 0
        self._animation_duration = 6
        self._dir = 1
        self._run = False
        self._force = 0
        self._hit = False
        self._live = True
        self.pop_sound = pygame.mixer.Sound("src/pop.mp3")


    def update(self, player, gravity, map_tiles, map_width, pixel, zoom, map_x, map_y):
        self._run = False

        if not self._attack and not self._hit:
            dx = player.get_x() - self._x
            dy = player.get_y() - self._y
            if abs(dx) < self._range:
                if dx > 0:
                    self._x += self._speed
                    self._dir = 1
                    self._run = True
                else:
                    self._x -= self._speed
                    self._dir = 0
                    self._run = True

        self._force += gravity
        self._y += self._force

        px = py = 0
        tooth_rect_y = pygame.Rect(self._x, self._y, self._dx*zoom, self._dy*zoom)
        for i in map_tiles:
            tile_rect = pygame.Rect(map_x + px, map_y + py, pixel, pixel)
            if i > 0 and tooth_rect_y.colliderect(tile_rect):
                self._y -= self._force
                self._force = 0
            px += pixel
            if px >= map_width * pixel:
                px = 0
                py += pixel

        player_rect = player.complete_hit_box_y(zoom)

        if player_rect.colliderect(tooth_rect_y):
            self._attack = True
            if player.get_attack():
                self.die()

        self._animation_timer += 1
        if self._animation_timer >= self._animation_duration:
            self._animation_timer = 0
            self._px += self._dx
            if self._px >= self._dx * self._max_frames:
                self._px = 0
                if self._hit:
                    self._live = False
                    self._px = self._dx * self._max_frames - self._dx
                if self._attack:
                    self._attack = False
                    if player_rect.colliderect(tooth_rect_y):
                        player.die()

        self._py = 0
        self._max_frames = 8
        if self._run:
            self._py = self._dy
            self._max_frames = 6
        if self._attack:
            self._py = self._dy * 3
            self._max_frames = 5
        if self._hit:
            self._py = self._dy * 2
            self._max_frames = 4


    def draw(self, screen, zoom):
        frame_rect = pygame.Rect(self._px, self._py, self._dx, self._dy)
        frame = self._img.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (self._dx * zoom, self._dy * zoom))

        if self._dir == 0:
            scaled_frame = pygame.transform.flip(scaled_frame, True, False)

        screen.blit(scaled_frame, (self._x, self._y))

    def die(self):
        self._hit = True
        self._animation_timer = 0
        self._force = -20
        self._px = 0
        self.pop_sound.play()

    def get_live(self):
        return self._live

    def set_volume(self, vol):
        self.pop_sound.set_volume(vol)

    def add_x(self, v): self._x += v
    def add_y(self, v): self._y += v
    def get_x(self): return self._x
    def get_y(self): return self._y
