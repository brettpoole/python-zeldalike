import pygame
import math
from settings import *
from tilemap import T_WATER, WALL_ONLY


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 28
        self.h = 28
        self.vx = 0.0
        self.vy = 0.0
        self.facing = "down"   # up/down/left/right

        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.xp = 0
        self.level = 1
        self.xp_to_next = XP_PER_LEVEL

        self.sword_timer = 0    # counts down while swinging
        self.sword_cd = 1       # cooldown after swing
        self.i_frames = 0       # invincibility frames

        self.anim_tick = 0
        self.walk_frame = 0
        self.alive = True
        self.in_water = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    @property
    def center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def sword_rect(self):
        cx, cy = self.center
        reach = TILE * 0.85
        sw, sh = 28, 28
        if self.facing == "right":
            return pygame.Rect(cx + 10, cy - sh // 2, reach, sh)
        if self.facing == "left":
            return pygame.Rect(cx - 10 - reach, cy - sh // 2, reach, sh)
        if self.facing == "down":
            return pygame.Rect(cx - sw // 2, cy + 10, sw, reach)
        return pygame.Rect(cx - sw // 2, cy - 10 - reach, sw, reach)

    def handle_input(self, keys):
        self.vx = 0.0
        self.vy = 0.0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.vx -= PLAYER_SPEED; self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.vx += PLAYER_SPEED; self.facing = "right"
        if keys[pygame.K_UP]    or keys[pygame.K_w]: self.vy -= PLAYER_SPEED; self.facing = "up"
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: self.vy += PLAYER_SPEED; self.facing = "down"

        # normalise diagonal
        if self.vx and self.vy:
            self.vx *= 0.7071
            self.vy *= 0.7071

        # attack (disabled in water)
        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and self.sword_cd == 0 and not self.in_water:
            self.sword_timer = SWORD_FRAMES
            self.sword_cd = SWORD_COOLDOWN

    def move(self, tilemap):
        # move X
        self.x += self.vx
        r = self.rect
        if tilemap.rect_blocked(r, WALL_ONLY):
            self.x -= self.vx

        # move Y
        self.y += self.vy
        r = self.rect
        if tilemap.rect_blocked(r, WALL_ONLY):
            self.y -= self.vy

        # clamp to world
        self.x = max(0, min(self.x, MAP_PX_W - self.w))
        self.y = max(0, min(self.y, MAP_PX_H - self.h))

        # water detection at feet
        cx_tile = int((self.x + self.w / 2) // TILE)
        cy_tile = int((self.y + self.h * 0.75) // TILE)
        self.in_water = tilemap.tile_at(cx_tile, cy_tile) == T_WATER

    def take_damage(self, amount, particles, texts, font):
        if self.i_frames > 0:
            return
        self.hp -= amount
        self.i_frames = I_FRAMES
        cx, cy = self.center
        particles.burst(cx, cy, C_DMG, count=10, speed=3)
        texts.append(type('FT', (), {
            'x': cx, 'y': cy - 16, 'text': f"-{amount}",
            'color': C_DMG, 'font': font, 'life': 40, 'max_life': 40,
            'update': lambda self: (setattr(self, 'y', self.y - 0.7),
                                    setattr(self, 'life', self.life - 1)),
            'draw': lambda self, surf, cx, cy: surf.blit(
                self.font.render(self.text, True, self.color),
                (int(self.x - cx), int(self.y - cy))
            )
        })())
        if self.hp <= 0:
            self.alive = False

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = XP_PER_LEVEL * self.level
            self.max_hp = min(PLAYER_MAX_HP + (self.level - 1) * 2, 12)
            self.hp = min(self.hp + 2, self.max_hp)

    def update(self, tilemap, keys):
        self.handle_input(keys)
        self.move(tilemap)
        if self.sword_timer > 0:
            self.sword_timer -= 1
        if self.sword_cd > 0:
            self.sword_cd -= 1
        if self.i_frames > 0:
            self.i_frames -= 1

        if self.vx != 0 or self.vy != 0:
            self.anim_tick += 1
            if self.anim_tick % 8 == 0:
                self.walk_frame = (self.walk_frame + 1) % 4

    def draw(self, surf, cam_x, cam_y):
        rx = int(self.x - cam_x)
        ry = int(self.y - cam_y)
        cx = rx + self.w // 2
        cy = ry + self.h // 2

        # flicker when invincible
        if self.i_frames > 0 and (self.i_frames // 4) % 2 == 1:
            return

        # body
        pygame.draw.ellipse(surf, C_PLAYER, (rx+2, ry+10, self.w-4, self.h-10))
        # head
        pygame.draw.circle(surf, C_PLAYER_LT, (cx, ry+8), 11)
        # hat / cap
        pygame.draw.ellipse(surf, (40, 80, 160), (cx-9, ry-2, 18, 8))
        pygame.draw.rect(surf,    (40, 80, 160), (cx-7, ry-8, 14, 10))
        # eyes
        ex_off = 0
        if self.facing == "right": ex_off = 3
        if self.facing == "left":  ex_off = -3
        if self.facing != "up":
            pygame.draw.circle(surf, C_BLACK, (cx + ex_off - 3, ry+8), 2)
            pygame.draw.circle(surf, C_BLACK, (cx + ex_off + 3, ry+8), 2)

        # water wading: cover lower body with semi-transparent water
        if self.in_water:
            waterline = ry + 15
            wade = pygame.Surface((self.w + 10, ry + self.h - waterline + 4),
                                   pygame.SRCALPHA)
            wade.fill((*C_WATER, 210))
            surf.blit(wade, (rx - 5, waterline))
            # ripple highlight at surface
            pygame.draw.ellipse(surf, C_WATER2,
                                (rx - 4, waterline - 3, self.w + 8, 6))

        # sword swing (blocked in water)
        if self.sword_timer > 0 and not self.in_water:
            self._draw_sword(surf, rx, ry, cx, cy)

    def _draw_sword(self, surf, rx, ry, cx, cy):
        prog = 1 - self.sword_timer / SWORD_FRAMES
        length = int(TILE * 0.85)
        thickness = 5
        if self.facing == "right":
            sx = cx + 10
            pygame.draw.rect(surf, C_SWORD,
                             (sx, cy - thickness // 2,
                              int(length * prog) + 8, thickness))
        elif self.facing == "left":
            sx = cx - 10
            w = int(length * prog) + 8
            pygame.draw.rect(surf, C_SWORD,
                             (sx - w, cy - thickness // 2, w, thickness))
        elif self.facing == "down":
            sy = cy + 10
            pygame.draw.rect(surf, C_SWORD,
                             (cx - thickness // 2, sy,
                              thickness, int(length * prog) + 8))
        else:
            sy = cy - 10
            h = int(length * prog) + 8
            pygame.draw.rect(surf, C_SWORD,
                             (cx - thickness // 2, sy - h, thickness, h))

    def draw_hud(self, surf, font_sm):
        # HUD background
        hud_w, hud_h = 220, 56
        hud = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
        hud.fill((20, 20, 30, 180))
        surf.blit(hud, (8, 8))

        # hearts
        heart_size = 18
        for i in range(self.max_hp):
            hx = 16 + (i % 6) * (heart_size + 4)
            hy = 14 + (i // 6) * (heart_size + 4)
            color = C_HEART_FULL if i < self.hp else C_HEART_EMPTY
            _draw_heart(surf, hx, hy, heart_size, color)

        # XP bar
        bar_x, bar_y, bar_w, bar_h = 16, 44, 190, 8
        pygame.draw.rect(surf, (40, 40, 60), (bar_x, bar_y, bar_w, bar_h))
        if self.xp_to_next > 0:
            fill = int(bar_w * self.xp / self.xp_to_next)
            pygame.draw.rect(surf, C_XP_BAR, (bar_x, bar_y, fill, bar_h))
        pygame.draw.rect(surf, C_WHITE, (bar_x, bar_y, bar_w, bar_h), 1)

        # level text
        lbl = font_sm.render(f"LV{self.level}", True, C_WHITE)
        surf.blit(lbl, (212, 40))


def _draw_heart(surf, x, y, size, color):
    s = size // 2
    pygame.draw.circle(surf, color, (x + s // 2, y + s // 2), s // 2)
    pygame.draw.circle(surf, color, (x + size - s // 2, y + s // 2), s // 2)
    pts = [(x, y + s // 2),
           (x + size // 2, y + size),
           (x + size, y + s // 2)]
    pygame.draw.polygon(surf, color, pts)
