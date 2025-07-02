from abc import ABC, abstractmethod

import pygame

class Player(ABC):
    def __init__(self, x, y, dx, dy, max_frames, img):
        self._x = x
        self._y = y
        self._speed = 8
        self._px = self._py = 0
        self._dx = dx
        self._dy = dy
        self._max_frames = max_frames
        self._animation_duration = 6
        self._animation_timer = 0
        self._force = 0
        self._dir = 1
        self._img = img
        self._run = False
        self._attack = False
        self._hit = False
        self._fall = False
        self._jump = False
        self._dead = False
        self._jump_count = 0
        self._under_water = None
        self._air = None
        self._air_count = None
        self._swim = False
        self._attack_allowed = True
        self._live = True
        self._finish = False
        self.jump_sound = pygame.mixer.Sound("src/jump.mp3")
        self.dead_sound = pygame.mixer.Sound("src/die.mp3")

    def update(self, gravity, map, map_width, pixel, zoom, map_x, map_y, water):
        self.action()

        #timer para delay entre frames na animação
        self._animation_timer += 1
        if self._animation_timer >= self._animation_duration:
            self._animation_timer = 0
            self._px += self._dx

            if self._px >= self._max_frames * self._dx:
                self._px = 0

                #para com a animação se for animação se for preciso
                if self._hit:
                    self._live = False
                    self._px = self._max_frames * self._dx - self._dx
                if self._attack:
                    self._attack = False
                if self._jump:
                    self._jump = False
                    self._fall = True

        #detecta ataque
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and not self._attack and not self._hit and not (self._fall or self._jump) and self._attack_allowed:
            self._attack = True
            self._px = 0
            self._animation_timer = 0

        if not mouse_buttons[0]:
            self._attack_allowed = True

        max_force = 20
        jump_force = 25
        self._swim = False

        #colisão com a agua
        px = py = 0
        player_rect = self.hit_box(zoom)
        for i in water:
            tile_rect = pygame.Rect(map_x+px, map_y+py, pixel, pixel)
            if (i == 102 or i == 103) and player_rect.colliderect(tile_rect):
                max_force = 5
                self._jump_count = 0
                jump_force = 15
                if not self._under_water:
                    self._swim = True
                break

            px += pixel
            if px >= map_width * pixel:
                px = 0
                py += pixel

        if self._swim or self._air < 11:
            self._air_count += 1

        if self._air_count >= 60:
            if self._swim:
                self._air -= 1
            else:
                self._air += 1
            self._air_count = 0

        if self._air <= 0:
            self.die()


        #movimentação
        if not self._attack and not self._hit:
            key = pygame.key.get_pressed()
            #pula
            if key[pygame.K_w] and self._jump_count == 0:
                self._jump = True
                self._fall = False
                self._px = 0
                self._jump_count = 1
                self._animation_timer = 0
                self._force = -jump_force
                if not self._under_water and not self._swim:
                    self.jump_sound.play()

            #desce rápido
            if key[pygame.K_s] and (self._fall or self._jump):
                self._fall = True
                self._jump = False
                if self._force < max_force:
                    self._force = max_force

            #anda
            if key[pygame.K_d]:
                self._x += self._speed
                self._dir = 1
                self._run = True
            elif key[pygame.K_a]:
                self._x -= self._speed
                self._dir = 0
                self._run = True
            else:
                self._run = False

        #limite da aceleração
        if self._force > max_force:
            self._force = max_force

        if self._force > 5 and  not self._fall:
            self._fall = True

        # gravidade
        self._force += gravity
        self._y += self._force

        # detectar colisões
        px = py = 0
        player_rect = self.hit_box(zoom)
        player_rectY = self.hit_box_y(zoom)
        for i in map:
            tile_rect = pygame.Rect(map_x+px, map_y+py, pixel, pixel)

            if i > 0 and player_rectY.colliderect(tile_rect):
                self._y -= self._force
                self._force = 0
                if self._fall:
                    self._fall = False
                    self._jump_count = 0
                    self._animation_timer = 0
                if i == 106:
                    self.die()
                if i == 109:
                    self._finish = True

            if (
                    i > 0
                    and player_rect.colliderect(tile_rect)
                    and player_rect.right > tile_rect.left
                    and self._dir == 1
                    and (self._run or self._attack)
            ):
                if self._attack:
                    self._attack = False
                    self._animation_timer = 0
                    self._attack_allowed = False
                self._x -= self._speed
                self._run = False

            if (
                    i > 0
                    and player_rect.colliderect(tile_rect)
                    and player_rect.left < tile_rect.left + pixel
                    and self._dir == 0
                    and (self._run or self._attack)
            ):
                if self._attack:
                    self._attack = False
                    self._animation_timer = 0
                    self._attack_allowed = False
                self._x += self._speed
                self._run = False

            px += pixel
            if px >= map_width * pixel:
                px = 0
                py += pixel

        self._py = 0
        self._max_frames = 5

        #animação de corrida
        if self._run:
            self._py = self._dy
            self._max_frames = 6

        #animação de ataque
        if self._attack:
            self._py = self._dy*5
            self._max_frames = 3

        #animação de hit
        if self._hit:
            self._py = self._dy*7
            self._max_frames = 4

        #animação de pulo
        if self._jump:
            self._py = self._dy*2
            self._max_frames = 3

        #animação de caida
        if self._fall:
            self._py = self._dy*3
            self._max_frames = 1


    def draw(self, screen, zoom):
        #Da zoom no personagem
        frame_rect = pygame.Rect(self._px, self._py, self._dx, self._dy)
        frame = self._img.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (self._dx * zoom, self._dy * zoom))

        #inverte o frame, caso o player estiver para esquerda
        if self._dir == 0:
            scaled_frame = pygame.transform.flip(scaled_frame, True, False)

        #desenha frame personalizado do personagem
        screen.blit(scaled_frame, (self._x, self._y))

    def die(self):
        self._force = -20
        self._animation_timer = 0
        self._hit = True
        self._px = 0
        self.dead_sound.set_volume(self.jump_sound.get_volume())
        self.dead_sound.play()


    def set_volume(self, vol):
        self.jump_sound.set_volume(vol)

    def get_x(self):
        return self._x
    def get_y(self):
        return self._y

    def get_img(self):
        return self._img

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        self._speed = speed

    def get_force(self):
        return self._force

    def get_live(self):
        return self._live

    def get_fall(self):
        return self._fall

    def get_jump(self):
        return self._jump

    def get_attack(self):
        return self._attack

    def get_finish(self):
        return self._finish

    def get_air(self):
        return self._air

    def set_x(self, x):
        self._x = x
    def set_y(self, y):
        self._y = y

    @abstractmethod
    def action(self):
        pass
    @abstractmethod
    def hit_box(self, zoom):
        pass
    @abstractmethod
    def hit_box_y(self, zoom):
        pass

    @abstractmethod
    def complete_hit_box_y(self, zoom):
        pass