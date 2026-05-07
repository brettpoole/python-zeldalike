import pygame
import sys
import math
from settings import *
from tilemap import TileMap, WORLD_MAP
from camera import Camera
from player import Player
from enemies import spawn_enemies
from particles import ParticleSystem, FloatingText


class FloatText:
    def __init__(self, x, y, text, color, font, life=40):
        self.x = float(x)
        self.y = float(y)
        self.text = text
        self.color = color
        self.font = font
        self.life = life
        self.max_life = life

    def update(self):
        self.y -= 0.7
        self.life -= 1

    def draw(self, surf, cam_x, cam_y):
        alpha = max(0, min(255, int(255 * self.life / self.max_life)))
        img = self.font.render(self.text, True, self.color)
        img.set_alpha(alpha)
        surf.blit(img,
                  (int(self.x - cam_x) - img.get_width() // 2,
                   int(self.y - cam_y)))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font_sm = pygame.font.SysFont("monospace", 13, bold=True)
        self.font_md = pygame.font.SysFont("monospace", 20, bold=True)
        self.font_lg = pygame.font.SysFont("monospace", 40, bold=True)

        self._new_game()

    def _new_game(self):
        self.tilemap  = TileMap()
        self.camera   = Camera()
        self.player   = Player(TILE * 2 + 4, TILE * 2 + 4)
        self.enemies  = spawn_enemies(WORLD_MAP, TILE)
        self.particles = ParticleSystem()
        self.float_texts: list[FloatText] = []
        self.hit_enemies: set[int] = set()  # ids already hit this swing
        self.state = "play"   # play / dead / levelup
        self.level_up_timer = 0
        self.tick = 0

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            self._handle_events()
            if self.state == "play":
                self._update()
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if self.state == "dead" and event.key == pygame.K_r:
                    self._new_game()
                if self.state == "levelup" and event.key in (
                        pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                    self.state = "play"

    def _update(self):
        self.tick += 1
        keys = pygame.key.get_pressed()
        prev_level = self.player.level

        self.player.update(self.tilemap, keys)

        # reset hit set when sword swing starts
        if self.player.sword_timer == SWORD_FRAMES - 1:
            self.hit_enemies.clear()

        sword_active = self.player.sword_timer > 0
        sword_r = self.player.sword_rect() if sword_active else None

        for enemy in self.enemies:
            enemy.update(self.tilemap, self.player)

            # sword → enemy
            if sword_active and id(enemy) not in self.hit_enemies:
                if sword_r.colliderect(enemy.rect):
                    enemy.take_hit(SWORD_DAMAGE)
                    self.hit_enemies.add(id(enemy))
                    self.particles.burst(
                        *enemy.center, C_DMG, count=8, speed=3)
                    self.float_texts.append(FloatText(
                        enemy.center[0], enemy.center[1] - 16,
                        f"-{SWORD_DAMAGE}", C_DMG, self.font_sm))
                    if not enemy.alive:
                        self.player.gain_xp(enemy.xp_value)
                        self.particles.burst(
                            *enemy.center, C_XP_BAR, count=12, speed=4)

            # enemy → player
            if (enemy.alive and enemy.attack_cd == 0
                    and enemy.rect.inflate(4, 4).colliderect(self.player.rect)):
                self.player.hp = max(0,
                    self.player.hp - enemy.damage if self.player.i_frames == 0
                    else self.player.hp)
                if self.player.i_frames == 0:
                    self.player.i_frames = I_FRAMES
                    self.particles.burst(
                        *self.player.center, C_DMG, count=10, speed=3)
                    self.float_texts.append(FloatText(
                        self.player.center[0],
                        self.player.center[1] - 16,
                        f"-{enemy.damage}", C_DMG, self.font_sm))
                    if self.player.hp <= 0:
                        self.state = "dead"
                enemy.attack_cd = 50

        # remove dead
        self.enemies = [e for e in self.enemies if e.alive]

        # float texts
        self.float_texts = [t for t in self.float_texts if t.life > 0]
        for t in self.float_texts:
            t.update()

        self.particles.update()
        self.camera.update(self.player.rect)

        # level-up notification
        if self.player.level > prev_level:
            self.state = "levelup"
            self.level_up_timer = 120

    def _draw(self):
        self.screen.fill(C_BLACK)
        cam_x, cam_y = self.camera.offset

        self.tilemap.draw(self.screen, self.camera.offset)

        # enemies (sorted by y for depth)
        for enemy in sorted(self.enemies, key=lambda e: e.y):
            enemy.draw(self.screen, cam_x, cam_y)

        self.player.draw(self.screen, cam_x, cam_y)
        self.particles.draw(self.screen, cam_x, cam_y)

        for t in self.float_texts:
            t.draw(self.screen, cam_x, cam_y)

        self.player.draw_hud(self.screen, self.font_sm)
        self._draw_minimap()

        if self.state == "dead":
            self._draw_overlay("YOU DIED", "(press R to restart)", (180, 40, 40))
        elif self.state == "levelup":
            self._draw_level_up()

        # controls hint (first 5 seconds)
        if self.tick < FPS * 5:
            hint = self.font_sm.render(
                "WASD/Arrows: move   Space/Z: attack   Esc: quit",
                True, C_WHITE)
            hint.set_alpha(200)
            self.screen.blit(hint,
                             (SCREEN_W // 2 - hint.get_width() // 2,
                              SCREEN_H - 28))

        pygame.display.flip()
        self.clock.tick(FPS)

    def _draw_minimap(self):
        scale = 4
        rows = len(WORLD_MAP)
        cols = len(WORLD_MAP[0])
        mm_w = cols * scale
        mm_h = rows * scale
        mm_x = SCREEN_W - mm_w - 10
        mm_y = 10

        mm = pygame.Surface((mm_w, mm_h))
        mm.set_alpha(180)
        from tilemap import T_WALL, T_WATER, T_GRASS, T_SAND, T_DIRT, T_DOOR
        MCOLORS = {
            T_GRASS: C_GRASS,
            T_WALL:  C_WALL,
            T_WATER: C_WATER,
            T_SAND:  C_SAND,
            T_DIRT:  C_DIRT,
            T_DOOR:  C_DOOR,
        }
        for row, tiles in enumerate(WORLD_MAP):
            for col, tid in enumerate(tiles):
                color = MCOLORS.get(tid, C_GRASS)
                mm.fill(color, (col * scale, row * scale, scale, scale))

        # enemies on minimap
        for e in self.enemies:
            ex = int(e.x / TILE * scale)
            ey = int(e.y / TILE * scale)
            mm.fill((220, 60, 60),
                    (max(0, ex), max(0, ey), max(2, scale-1), max(2, scale-1)))

        # player dot
        px = int(self.player.x / TILE * scale)
        py = int(self.player.y / TILE * scale)
        pygame.draw.rect(mm, C_PLAYER_LT, (px-1, py-1, 4, 4))

        pygame.draw.rect(self.screen, C_WALL,
                         (mm_x-1, mm_y-1, mm_w+2, mm_h+2), 1)
        self.screen.blit(mm, (mm_x, mm_y))

    def _draw_overlay(self, title, subtitle, color):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        t1 = self.font_lg.render(title, True, color)
        t2 = self.font_md.render(subtitle, True, C_WHITE)
        self.screen.blit(t1, (SCREEN_W // 2 - t1.get_width() // 2,
                               SCREEN_H // 2 - 50))
        self.screen.blit(t2, (SCREEN_W // 2 - t2.get_width() // 2,
                               SCREEN_H // 2 + 10))

    def _draw_level_up(self):
        banner = self.font_lg.render(
            f"LEVEL {self.player.level}!", True, (255, 220, 60))
        sub = self.font_md.render(
            "HP increased!  Press Space to continue", True, C_WHITE)
        bx = SCREEN_W // 2 - banner.get_width() // 2
        by = SCREEN_H // 2 - 40
        pygame.draw.rect(self.screen, (20, 20, 40),
                         (bx - 16, by - 8,
                          banner.get_width() + 32,
                          banner.get_height() + sub.get_height() + 24))
        self.screen.blit(banner, (bx, by))
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2,
                                by + banner.get_height() + 8))
