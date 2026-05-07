import pygame
import math
import random
from settings import *
from particles import FloatingText
from tilemap import WALL_ONLY


class Enemy:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 26
        self.h = 26
        self.vx = 0.0
        self.vy = 0.0
        self.hp = 10
        self.max_hp = 10
        self.damage = 1
        self.speed = 1.0
        self.xp_value = 10
        self.alive = True
        self.hit_flash = 0      # frames of white flash after being hit
        self.anim_tick = 0
        self.state = "wander"   # wander / chase
        self.state_timer = random.randint(30, 90)
        self.wander_dx = random.choice([-1, 0, 0, 1])
        self.wander_dy = random.choice([-1, 0, 0, 1])
        self.attack_cd = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    @property
    def center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def _dist_to_player(self, px, py):
        cx, cy = self.center
        return math.hypot(cx - px, cy - py)

    def update(self, tilemap, player):
        self.anim_tick += 1
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.attack_cd > 0:
            self.attack_cd -= 1

        px, py = player.center
        dist = self._dist_to_player(px, py)

        # state machine
        if dist < TILE * 5:
            self.state = "chase"
        elif dist > TILE * 7:
            self.state = "wander"
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state_timer = random.randint(30, 90)
                self.wander_dx = random.choice([-1, 0, 0, 1])
                self.wander_dy = random.choice([-1, 0, 0, 1])

        if self.state == "chase":
            cx, cy = self.center
            dx = px - cx
            dy = py - cy
            length = math.hypot(dx, dy) or 1
            self.vx = dx / length * self.speed
            self.vy = dy / length * self.speed
        else:
            self.vx = self.wander_dx * self.speed * 0.5
            self.vy = self.wander_dy * self.speed * 0.5

        self._move(tilemap)

    def _move(self, tilemap):
        self.x += self.vx
        if tilemap.rect_blocked(self.rect):
            self.x -= self.vx
            self.wander_dx = -self.wander_dx
        self.y += self.vy
        if tilemap.rect_blocked(self.rect):
            self.y -= self.vy
            self.wander_dy = -self.wander_dy

        self.x = max(0, min(self.x, MAP_PX_W - self.w))
        self.y = max(0, min(self.y, MAP_PX_H - self.h))

    def take_hit(self, damage):
        self.hp -= damage
        self.hit_flash = 8
        if self.hp <= 0:
            self.alive = False

    def draw_health_bar(self, surf, rx, ry):
        if self.hp == self.max_hp:
            return
        bar_w = self.w
        filled = int(bar_w * self.hp / self.max_hp)
        pygame.draw.rect(surf, (80, 20, 20), (rx, ry - 6, bar_w, 4))
        pygame.draw.rect(surf, (220, 60, 60), (rx, ry - 6, filled, 4))


class Slime(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = SLIME_HP
        self.max_hp = SLIME_HP
        self.damage = SLIME_DAMAGE
        self.speed = SLIME_SPEED
        self.xp_value = SLIME_XP
        self.hop_timer = 0

    def draw(self, surf, cam_x, cam_y):
        rx = int(self.x - cam_x)
        ry = int(self.y - cam_y)
        # hop animation
        hop = -abs(math.sin(self.anim_tick * 0.15)) * 5
        color = C_WHITE if self.hit_flash else C_SLIME
        dk = C_WHITE if self.hit_flash else C_SLIME_DK
        # shadow
        pygame.draw.ellipse(surf, (0, 0, 0, 80),
                            (rx+4, ry+self.h-6, self.w-8, 6))
        # body
        pygame.draw.ellipse(surf, dk,
                            (rx, ry+hop+8, self.w, self.h-8))
        pygame.draw.ellipse(surf, color,
                            (rx+2, ry+hop+6, self.w-4, self.h-10))
        # eyes
        ex = rx + 7
        ey = int(ry + hop + 8)
        pygame.draw.circle(surf, C_WHITE, (ex, ey), 4)
        pygame.draw.circle(surf, C_WHITE, (ex+12, ey), 4)
        pygame.draw.circle(surf, C_BLACK, (ex+1, ey), 2)
        pygame.draw.circle(surf, C_BLACK, (ex+13, ey), 2)
        self.draw_health_bar(surf, rx, ry)


class Skull(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = SKULL_HP
        self.max_hp = SKULL_HP
        self.damage = SKULL_DAMAGE
        self.speed = SKULL_SPEED
        self.xp_value = SKULL_XP
        self.w = 28
        self.h = 28

    def draw(self, surf, cam_x, cam_y):
        rx = int(self.x - cam_x)
        ry = int(self.y - cam_y)
        bob = int(math.sin(self.anim_tick * 0.12) * 3)
        color = C_WHITE if self.hit_flash else C_SKULL
        dk = C_WHITE if self.hit_flash else C_SKULL_DK
        # skull
        pygame.draw.circle(surf, color, (rx+14, ry+14+bob), 13)
        # jaw
        pygame.draw.rect(surf, dk, (rx+5, ry+20+bob, 18, 8))
        # teeth
        for tx in (rx+6, rx+11, rx+16, rx+21):
            pygame.draw.rect(surf, C_WHITE, (tx, ry+20+bob, 3, 5))
        # eyes
        pygame.draw.ellipse(surf, C_BLACK, (rx+5, ry+10+bob, 8, 7))
        pygame.draw.ellipse(surf, C_BLACK, (rx+15, ry+10+bob, 8, 7))
        pygame.draw.ellipse(surf, (255, 60, 60), (rx+6, ry+11+bob, 5, 4))
        pygame.draw.ellipse(surf, (255, 60, 60), (rx+16, ry+11+bob, 5, 4))
        self.draw_health_bar(surf, rx, ry)


class Bat(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = BAT_HP
        self.max_hp = BAT_HP
        self.damage = BAT_DAMAGE
        self.speed = BAT_SPEED
        self.xp_value = BAT_XP
        self.w = 30
        self.h = 20

    def _move(self, tilemap):
        self.x += self.vx
        if tilemap.rect_blocked(self.rect, WALL_ONLY):
            self.x -= self.vx
            self.wander_dx = -self.wander_dx
        self.y += self.vy
        if tilemap.rect_blocked(self.rect, WALL_ONLY):
            self.y -= self.vy
            self.wander_dy = -self.wander_dy
        self.x = max(0, min(self.x, MAP_PX_W - self.w))
        self.y = max(0, min(self.y, MAP_PX_H - self.h))

    def draw(self, surf, cam_x, cam_y):
        rx = int(self.x - cam_x)
        ry = int(self.y - cam_y)
        flap = int(math.sin(self.anim_tick * 0.3) * 5)
        color = C_WHITE if self.hit_flash else C_BAT
        dk = C_WHITE if self.hit_flash else C_BAT_DK
        # wings
        pygame.draw.ellipse(surf, dk,
                            (rx, ry+flap, 14, 12))
        pygame.draw.ellipse(surf, dk,
                            (rx+16, ry+flap, 14, 12))
        # body
        pygame.draw.ellipse(surf, color, (rx+9, ry+4, 12, 12))
        # eyes
        pygame.draw.circle(surf, (255, 100, 100), (rx+11, ry+7), 2)
        pygame.draw.circle(surf, (255, 100, 100), (rx+18, ry+7), 2)
        self.draw_health_bar(surf, rx, ry)


def spawn_enemies(world_map, tile_size):
    """Return a list of enemies placed in open areas of the map."""
    enemies = []
    rows = len(world_map)
    cols = len(world_map[0])
    from tilemap import SOLID
    for row in range(2, rows - 2):
        for col in range(2, cols - 2):
            if world_map[row][col] in SOLID:
                continue
            if random.random() < 0.04:
                ex = col * tile_size + tile_size // 4
                ey = row * tile_size + tile_size // 4
                # don't spawn too close to start
                if ex < tile_size * 3 and ey < tile_size * 3:
                    continue
                roll = random.random()
                if roll < 0.5:
                    enemies.append(Slime(ex, ey))
                elif roll < 0.75:
                    enemies.append(Skull(ex, ey))
                else:
                    enemies.append(Bat(ex, ey))
    return enemies
