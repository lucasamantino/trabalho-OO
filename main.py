import pygame
import json

from enemies.idle_enemy import IdleEnemy
from enemies.tooth import Tooth
from obj.item import Item
from obj.shoot import Shoot
from players.pirate import Pirate
from maps.map import Map
from players.star import Star

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption("Treasure")
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.mixer.init()
        pygame.mixer.music.load("src/music.mp3")
        pygame.mixer.music.play(-1)

        self.music_volume = 1
        self.efeito_volume = 1

        self.font = pygame.font.Font("src/main.ttf", 64)
        self.zoom = 4
        self.gravity = 1
        self.pixel = 32
        self.coin_count = 0

        self.keep = False

        self.paused = False

        self.victory_page = False

        original = pygame.image.load("src/bubble.png").convert_alpha()
        w = int(original.get_width() * 3)
        h = int(original.get_height() * 3)
        self._bubble_img = pygame.transform.scale(original, (w, h))

        self.map = None
        self.player = None

        self.last_level = 0
        self.select = 0

        self.coins_memory = 0

        self.items = []

        self.smart_enemies = []
        self.idle_enemies = []

        self.mouse_clicked = False

        self.game_overed = False

        self.shoots = []

        original = pygame.image.load("src/background.png").convert()
        regx = self.screen.get_width()/384
        regy = self.screen.get_height()/128
        w = int(original.get_width() * regx)
        h = int(original.get_height() * regy)
        self.background = pygame.transform.scale(original, (w, h))

        self.menu_page = True
        original = pygame.image.load("src/background-menu.png").convert_alpha()
        regx = self.screen.get_width()/954
        regy = self.screen.get_height()/573
        w = int(original.get_width() * regx)
        h = int(original.get_height() * regy)
        self.menu_background = pygame.transform.scale(original, (w, h))

        original = pygame.image.load("src/menu.png").convert_alpha()
        w = int(original.get_width() * 4)
        h = int(original.get_height() * 4)
        self.menu_display = pygame.transform.scale(original, (w, h))

        original = pygame.image.load("src/play.png").convert_alpha()
        w = int(original.get_width() * 5)
        h = int(original.get_height() * 5)
        self.play_btn = pygame.transform.scale(original, (w, h))

        original = pygame.image.load("src/level-background.png").convert_alpha()
        w = int(original.get_width() * 5)
        h = int(original.get_height() * 5)
        self.level_background = pygame.transform.scale(original, (w, h))

        original = pygame.image.load("src/level1.png").convert_alpha()
        self.level1_btn = pygame.transform.scale(original, (int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/level2.png").convert_alpha()
        self.level2_btn = pygame.transform.scale(original, (int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/level3.png").convert_alpha()
        self.level3_btn = pygame.transform.scale(original, (int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/select.png").convert_alpha()
        self.select_btn = pygame.transform.scale(original,(int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/player-background.png").convert_alpha()
        self.player_background = pygame.transform.scale(original,(int(original.get_width() * 5), int(original.get_height() * 5)))

        self.player_selected = 1

        original = pygame.image.load("src/player1.png").convert_alpha()
        self.player_opt_1 = pygame.transform.scale(original,(int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/player2.png").convert_alpha()
        self.player_opt_2 = pygame.transform.scale(original,(int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/coin-background.png").convert_alpha()
        self.coin_background = pygame.transform.scale(original,(int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/pause.png").convert_alpha()
        self.pause_display = pygame.transform.scale(original,(int(original.get_width() * 9), int(original.get_height() * 9)))

        original = pygame.image.load("src/continuar.png").convert_alpha()
        self.continuar_banner = pygame.transform.scale(original,(int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/menu-banner.png").convert_alpha()
        self.menu_banner = pygame.transform.scale(original,(int(original.get_width() * 5), int(original.get_height() * 5)))

        original = pygame.image.load("src/game-over.png").convert_alpha()
        self.game_over_display = pygame.transform.scale(original,(int(original.get_width() * 9), int(original.get_height() * 9)))

        original = pygame.image.load("src/vitoria-background.png").convert_alpha()
        self.victory_display = pygame.transform.scale(original,(int(original.get_width() * 9), int(original.get_height() * 9)))

        original = pygame.image.load("src/left.png").convert_alpha()
        self.left_arrow = pygame.transform.scale(original,(int(original.get_width() * 4), int(original.get_height() * 4)))
        original = pygame.image.load("src/right.png").convert_alpha()
        self.right_arrow = pygame.transform.scale(original,(int(original.get_width() * 4), int(original.get_height() * 4)))

        self.carregar()

    def start_var(self, num, type):
        self.coin_count = 0
        self.paused = False

        self.game_overed = False

        self.victory_page = False

        self.menu_page = False

        self.items = []
        self.smart_enemies = []
        self.idle_enemies = []
        self.shoots = []

        self.keep = False

        self.map = Map(num, self.zoom)

        if type == 2:
            self.player = Star(512,512, pygame)
        else:
            self.player = Pirate(512, 512, pygame)

        px = 0
        py = 0
        for it in self.map.get_treasures():
            if it == 108:
                self.items.append(Item(px+8, py+8, 1))
            if it == 106:
                self.items.append(Item(px+8, py+8, 2))

            px += self.pixel*self.zoom
            if px >= self.map.get_width() * self.pixel*self.zoom:
                px = 0
                py += self.pixel*self.zoom

        px = 0
        py = 0
        for it in self.map.get_enemies():
            if it == 110:
                self.idle_enemies.append(IdleEnemy(px,py+6*self.zoom, 1, 0))
            if it == 111:
                self.idle_enemies.append(IdleEnemy(px,py+6*self.zoom, 1, 1))

            if it == 112:
                self.idle_enemies.append(IdleEnemy(px,py-6*self.zoom, 2, 1))
            if it == 113:
                self.idle_enemies.append(IdleEnemy(px,py-6*self.zoom, 2, 0))

            if it == 153:
                self.smart_enemies.append(Tooth(px,py))

            px += self.pixel*self.zoom
            if px >= self.map.get_width() * self.pixel*self.zoom:
                px = 0
                py += self.pixel*self.zoom

    def update(self):
        self.player.update(self.gravity, self.map.get_tiles(), self.map.get_width(), self.pixel * self.zoom, self.zoom, self.map.get_x(), self.map.get_y(), self.map.get_water())

        self.player.set_volume(self.efeito_volume)

        if self.player.get_x() > self.screen.get_width() / 2 and abs(self.map.get_x()) + self.screen.get_width() + self.player.get_speed() < self.map.get_width() * self.pixel * self.zoom:
            self.map.addx(-self.player.get_speed())
            self.player.set_x(self.player.get_x() - self.player.get_speed())
            for it in self.items:
                it.add_x(-self.player.get_speed())
            for it in self.idle_enemies:
                it.add_x(-self.player.get_speed())
            for it in self.shoots:
                it.add_x(-self.player.get_speed())
            for it in self.smart_enemies:
                it.add_x(-self.player.get_speed())

        if self.player.get_x() < self.screen.get_width()/3 and self.map.get_x() < 0:
            self.map.addx(self.player.get_speed())
            self.player.set_x(self.player.get_x()+self.player.get_speed())
            for it in self.items:
                it.add_x(self.player.get_speed())
            for it in self.idle_enemies:
                it.add_x(self.player.get_speed())
            for it in self.shoots:
                it.add_x(self.player.get_speed())
            for it in self.smart_enemies:
                it.add_x(self.player.get_speed())

        if (self.player.get_y() > self.screen.get_height() - self.screen.get_height() / 2 and self.player.get_fall() and abs(self.map.get_y()) + self.screen.get_height() < self.map.get_height() * self.pixel * self.zoom):
            deslocamento = self.player.get_force()
            self.map.addy(-deslocamento)
            self.player.set_y(self.player.get_y() - deslocamento)
            for it in self.items:
                it.add_y(-deslocamento)
            for it in self.idle_enemies:
                it.add_y(-deslocamento)
            for it in self.shoots:
                it.add_y(-deslocamento)
            for it in self.smart_enemies:
                it.add_y(-deslocamento)

        if self.player.get_y() < self.screen.get_height()/3 and self.map.get_y() < 0 and self.player.get_jump():
            self.map.addy(-self.player.get_force())
            self.player.set_y(self.player.get_y()-self.player.get_force())
            for it in self.items:
                it.add_y(-self.player.get_force())
            for it in self.idle_enemies:
                it.add_y(-self.player.get_force())
            for it in self.shoots:
                it.add_y(-self.player.get_force())
            for it in self.smart_enemies:
                it.add_y(-self.player.get_force())

        for it in self.items[:]:
            it.update()

            player_rect = self.player.hit_box_y(self.zoom)
            coin_rect = pygame.Rect(it.get_x(), it.get_y(), 32, 32)
            if player_rect.colliderect(coin_rect):
                if it.get_type() == 1: self.coin_count += 1
                if it.get_type() == 2: self.keep = True
                self.items.remove(it)

        for enemy in self.idle_enemies:
            if enemy.update():
                if enemy.get_type() == 1:
                    self.shoots.append(Shoot(enemy.get_x() + self.pixel / 2, enemy.get_y(), 1, enemy.get_dir()))
                else:
                    self.shoots.append(Shoot(enemy.get_x() + self.pixel / 2, enemy.get_y()+self.pixel, 2, enemy.get_dir()))

        for shoot in self.shoots[:]:
            shoot.update()

            player_rect = self.player.hit_box_y(self.zoom)
            shoot_rect = pygame.Rect(shoot.get_x(), shoot.get_y(), 30, 30)

            if player_rect.colliderect(shoot_rect):
                self.player.die()
                self.shoots.remove(shoot)

            if shoot.get_x() > self.screen.get_width() or shoot.get_x() <0:
                self.shoots.remove(shoot)

        for smart in self.smart_enemies[:]:
            smart.update(self.player, self.gravity, self.map.get_tiles(), self.map.get_width(), self.pixel * self.zoom, self.zoom, self.map.get_x(), self.map.get_y())
            if not smart.get_live():
                self.smart_enemies.remove(smart)
            smart.set_volume(self.efeito_volume)

        if not self.player.get_live():
            self.game_overed = True
        if self.player.get_finish():
            if self.last_level <3:
                if (self.last_level == 1 and self.keep) or self.last_level > 1:
                    self.last_level += 1
            self.coins_memory += self.coin_count
            self.save()
            self.select = self.last_level
            self.victory_page = True

    def render(self):
        self.screen.blit(self.background, (0, 0))

        self.map.draw(self.screen)

        self.player.draw(self.screen, self.zoom)

        for it in self.items:
            it.draw(self.screen, self.zoom)

        for enemy in self.idle_enemies:
            enemy.draw(self.screen, self.zoom)

        for shoot in self.shoots:
            shoot.draw(self.screen, self.zoom)

        for smart in self.smart_enemies[:]:
            smart.draw(self.screen, self.zoom)

        self.map.draw_top(self.screen)

        self.screen.blit(self.font.render(f"{self.coin_count}/{self.map.get_coins()}", True, (255, 255, 255)), (self.screen.get_width()-150, 20))

        if self.player.get_air() <11:
            px = 15
            for i in range(self.player.get_air()):
                self.screen.blit(self._bubble_img, (px, 20))
                px += 16*3 + 4

        pygame.display.flip()

    def menu(self):
        self.screen.blit(self.menu_background, (0, 0))

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        menu_x = screen_w // 2 - self.menu_display.get_width() // 2
        menu_y = screen_h // 2 - self.menu_display.get_height() // 2
        self.screen.blit(self.menu_display, (menu_x, menu_y))

        play_x = screen_w // 2 - self.play_btn.get_width() // 2
        play_y = screen_h // 2 - self.play_btn.get_height() // 2 + 128
        self.screen.blit(self.play_btn, (play_x, play_y))

        level_x = screen_w // 2 - self.level_background.get_width() // 2 + self.menu_display.get_width()
        level_y = screen_h // 2 - self.level_background.get_height() // 2
        self.screen.blit(self.level_background, (level_x, level_y))

        lvl1_x = screen_w // 2 - self.level1_btn.get_width() // 2 + self.menu_display.get_width()
        lvl1_y = screen_h // 2 - self.level1_btn.get_height() // 2 - self.level_background.get_height() // 3
        self.screen.blit(self.level1_btn, (lvl1_x, lvl1_y))

        lvl2_x = screen_w // 2 - self.level2_btn.get_width() // 2 + self.menu_display.get_width()
        lvl2_y = screen_h // 2 - self.level2_btn.get_height() // 2
        self.screen.blit(self.level2_btn, (lvl2_x, lvl2_y))

        lvl3_x = screen_w // 2 - self.level3_btn.get_width() // 2 + self.menu_display.get_width()
        lvl3_y = screen_h // 2 - self.level3_btn.get_height() // 2 + self.level_background.get_height() // 3
        self.screen.blit(self.level3_btn, (lvl3_x, lvl3_y))

        select_y = screen_h // 2 - self.select_btn.get_height() // 2 - self.level_background.get_height() // 3 + (self.select - 1) * (self.level_background.get_height() // 3)
        select_x = screen_w // 2 - self.select_btn.get_width() // 2 + self.menu_display.get_width()
        self.screen.blit(self.select_btn, (select_x, select_y))

        PBK_x = screen_w // 2 - self.player_background.get_width() // 2
        PBK_y = screen_h // 2 - self.player_background.get_height() // 2 - self.menu_display.get_height() // 2 - self.player_background.get_height() // 2
        self.screen.blit(self.player_background, (PBK_x, PBK_y))

        if self.player_selected == 1:
            PBK_x = screen_w // 2 - self.player_opt_1.get_width() // 2
            PBK_y = screen_h // 2 - self.player_opt_1.get_height() // 2 - self.menu_display.get_height() // 2 - self.player_opt_1.get_height() // 2
            self.screen.blit(self.player_opt_1, (PBK_x, PBK_y))
        else:
            PBK_x = screen_w // 2 - self.player_opt_2.get_width() // 2
            PBK_y = screen_h // 2 - self.player_opt_2.get_height() // 2 - self.menu_display.get_height() // 2 - self.player_opt_2.get_height() + 45
            self.screen.blit(self.player_opt_2, (PBK_x, PBK_y))

        CBG_x = screen_w // 2 - self.coin_background.get_width() // 2 - self.coin_background.get_width() // 2 - self.menu_display.get_width() // 2
        CBG_y = screen_h // 2 - self.coin_background.get_height() // 2 - self.menu_display.get_height() // 2
        self.screen.blit(self.coin_background, (CBG_x, CBG_y))

        self.screen.blit(self.font.render(f"{self.coins_memory}", True, (255, 255, 255)), (CBG_x + self.coin_background.get_width()//3, CBG_y + 50))

        PBK2_x = screen_w // 2 - self.player_background.get_width() - 250
        PBK2_y = screen_h // 2 - self.player_background.get_height() // 2 - self.menu_display.get_height() // 2 + self.player_background.get_height()
        self.screen.blit(self.player_background, (PBK2_x, PBK2_y))

        LF1_x = screen_w // 2 - self.left_arrow.get_width() - 150 - self.player_background.get_width()
        LF1_y = screen_h // 2 - self.left_arrow.get_height() // 2 - self.menu_display.get_height() // 2 + 180
        self.screen.blit(self.left_arrow, (LF1_x, LF1_y))

        RG1_x = screen_w // 2 - self.right_arrow.get_width() - 300
        RG1_y = screen_h // 2 - self.right_arrow.get_height() // 2 - self.menu_display.get_height() // 2 + 180
        self.screen.blit(self.right_arrow, (RG1_x, RG1_y))

        self.screen.blit(self.font.render(f"{int(self.music_volume*100)}", True, (255, 255, 255)),(screen_w // 2 - self.right_arrow.get_width() - 465, screen_h // 2 - self.right_arrow.get_height() // 2 - self.menu_display.get_height() // 2 + 165))

        LF2_x = screen_w // 2 - self.left_arrow.get_width() - 150 - self.player_background.get_width()
        LF2_y = screen_h // 2 - self.left_arrow.get_height() // 2 - self.menu_display.get_height() // 2 + 260
        self.screen.blit(self.left_arrow, (LF2_x, LF2_y))

        RG2_x = screen_w // 2 - self.right_arrow.get_width() - 300
        RG2_y = screen_h // 2 - self.right_arrow.get_height() // 2 - self.menu_display.get_height() // 2 + 260
        self.screen.blit(self.right_arrow, (RG2_x, RG2_y))

        self.screen.blit(self.font.render(f"{int(self.efeito_volume * 100)}", True, (255, 255, 255)),
                         (screen_w // 2 - self.right_arrow.get_width() - 465,
                          screen_h // 2 - self.right_arrow.get_height() // 2 - self.menu_display.get_height() // 2 + 240))

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            left1_rect = pygame.Rect(LF1_x, LF1_y, self.left_arrow.get_width(), self.left_arrow.get_height())
            if left1_rect.collidepoint(mouse_pos) and self.music_volume > 0:
                self.music_volume = max(0, round(self.music_volume - 0.01, 2))

            right1_rect = pygame.Rect(RG1_x, RG1_y, self.right_arrow.get_width(), self.right_arrow.get_height())
            if right1_rect.collidepoint(mouse_pos) and self.music_volume < 100:
                self.music_volume = min(1, round(self.music_volume + 0.01, 2))

            left2_rect = pygame.Rect(LF2_x, LF2_y, self.left_arrow.get_width(), self.left_arrow.get_height())
            if left2_rect.collidepoint(mouse_pos) and self.efeito_volume > 0:
                self.efeito_volume = max(0, round(self.efeito_volume - 0.01, 2))

            right2_rect = pygame.Rect(RG2_x, RG2_y, self.right_arrow.get_width(), self.right_arrow.get_height())
            if right2_rect.collidepoint(mouse_pos) and self.efeito_volume < 100:
                self.efeito_volume = min(1, round(self.efeito_volume + 0.01, 2))

            play_rect = pygame.Rect(play_x, play_y, self.play_btn.get_width(), self.play_btn.get_height())
            if play_rect.collidepoint(mouse_pos):
                self.menu_page = False
                self.start_var(self.select, self.player_selected)

            lvl1_rect = pygame.Rect(lvl1_x, lvl1_y, self.level1_btn.get_width(), self.level1_btn.get_height())
            if lvl1_rect.collidepoint(mouse_pos):
                self.select = 1

            lvl2_rect = pygame.Rect(lvl2_x, lvl2_y, self.level2_btn.get_width(), self.level2_btn.get_height())
            if lvl2_rect.collidepoint(mouse_pos) and self.last_level >= 2:
                self.select = 2

            lvl3_rect = pygame.Rect(lvl3_x, lvl3_y, self.level3_btn.get_width(), self.level3_btn.get_height())
            if lvl3_rect.collidepoint(mouse_pos) and self.last_level >= 3:
                self.select = 3
            if not self.mouse_clicked:
                self.mouse_clicked = True
                player_rect = pygame.Rect(PBK_x, PBK_y, self.player_opt_1.get_width(), self.player_opt_1.get_height())
                if player_rect.collidepoint(mouse_pos):
                    if self.player_selected == 1:
                        self.player_selected = 2
                    else:
                        self.player_selected = 1
        else:
            self.mouse_clicked = False

    def pause(self):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        pause_x = screen_w // 2 - self.pause_display.get_width() // 2
        pause_y = screen_h // 2 - self.pause_display.get_height() // 2
        self.screen.blit(self.pause_display, (pause_x, pause_y))

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        continuar_banner_x = screen_w // 2 - self.continuar_banner.get_width()
        continuar_banner_y = screen_h // 2 - self.continuar_banner.get_height() // 2
        self.screen.blit(self.continuar_banner, (continuar_banner_x, continuar_banner_y))

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        menu_banner_x = screen_w // 2
        menu_banner_y = screen_h // 2 + self.menu_banner.get_height()
        self.screen.blit(self.menu_banner, (menu_banner_x, menu_banner_y))

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            banner_rect = pygame.Rect(continuar_banner_x, continuar_banner_y, self.continuar_banner.get_width(), self.continuar_banner.get_height())
            if banner_rect.collidepoint(mouse_pos):
                self.paused = False

            banner_rect = pygame.Rect(menu_banner_x, menu_banner_y, self.menu_banner.get_width(),
                                      self.menu_banner.get_height())
            if banner_rect.collidepoint(mouse_pos):
                self.paused = False
                self.menu_page = True

    def game_over(self):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        game_over_display_x = screen_w // 2 - self.game_over_display.get_width() // 2
        game_over_display_y = screen_h // 2 - self.game_over_display.get_height() // 2
        self.screen.blit(self.game_over_display, (game_over_display_x, game_over_display_y))

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        menu_banner_x = screen_w // 2
        menu_banner_y = screen_h // 2 + self.menu_banner.get_height()*2
        self.screen.blit(self.menu_banner, (menu_banner_x, menu_banner_y))

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            banner_rect = pygame.Rect(menu_banner_x, menu_banner_y, self.menu_banner.get_width(),
                                      self.menu_banner.get_height())
            if banner_rect.collidepoint(mouse_pos):
                self.paused = False
                self.menu_page = True

    def victory(self):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        victory_display_x = screen_w // 2 - self.victory_display.get_width() // 2
        victory_display_y = screen_h // 2 - self.victory_display.get_height() // 2
        self.screen.blit(self.victory_display, (victory_display_x, victory_display_y))

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        menu_banner_x = screen_w // 2
        menu_banner_y = screen_h // 2 + self.menu_banner.get_height()*2
        self.screen.blit(self.menu_banner, (menu_banner_x, menu_banner_y))

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0]:
            banner_rect = pygame.Rect(menu_banner_x, menu_banner_y, self.menu_banner.get_width(), self.menu_banner.get_height())
            if banner_rect.collidepoint(mouse_pos):
                self.paused = False
                self.menu_page = True

    def save(self):
        dados = {
            "coins" : self.coins_memory,
            "last_level" : self.last_level,
            "player" : self.player_selected,
            "music_volume" : self.music_volume,
            "efeito_volume" : self.efeito_volume
        }
        with open("data.json", "w") as f:
            json.dump(dados, f)

    def carregar(self):
        try:
            with open("data.json", "r") as f:
                dados = json.load(f)
                self.coins_memory = dados.get("coins", 0)
                self.last_level = dados.get("last_level", 1)
                self.player_selected = dados.get("player_selected", 1)
                self.music_volume = dados.get("music_volume", 1)
                self.efeito_volume = dados.get("efeito_volume", 1)
                self.select = self.last_level
        except FileNotFoundError:
            raise FileNotFoundError("Save não encontrado")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused

            pygame.mixer.music.set_volume(self.music_volume)

            if self.menu_page:
                self.menu()
            elif self.game_overed:
                self.game_over()
            elif self.victory_page:
                self.victory()
            elif not self.paused and self.player:
                self.update()
                self.render()
            elif self.paused:
                self.pause()

            pygame.display.flip()

            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
