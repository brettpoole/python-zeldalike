import pygame
from settings import *

# Tile IDs
T_GRASS  = 0
T_WALL   = 1
T_WATER  = 2
T_SAND   = 3
T_DIRT   = 4
T_DOOR   = 5

SOLID     = {T_WALL, T_WATER}
WALL_ONLY = frozenset({T_WALL})   # passable by player & bats
DEEP      = {T_WATER}

# ── World map (20 cols × 44 rows) ──────────────────────────────────────────
WORLD_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,5,4,1,0,0,3,3,0,0,1,4,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,4,1,0,0,3,3,0,0,1,4,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,4,1,0,0,0,0,0,0,1,4,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,5,4,5,0,0,3,3,0,0,5,4,5,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,4,1,0,0,3,3,0,0,1,4,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,4,4,4,4,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,4,4,4,4,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,4,4,4,4,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,4,4,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,4,4,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

MAP_COLS = len(WORLD_MAP[0])
MAP_ROWS = len(WORLD_MAP)
MAP_PX_W = MAP_COLS * TILE
MAP_PX_H = MAP_ROWS * TILE


def _draw_wall(surf, rx, ry):
    pygame.draw.rect(surf, C_WALL, (rx, ry, TILE, TILE))
    pygame.draw.rect(surf, C_WALL_LT, (rx+2, ry+2, TILE-4, 10))
    pygame.draw.rect(surf, C_WALL_LT, (rx+2, ry+16, TILE-4, 10))
    pygame.draw.line(surf, C_BLACK, (rx, ry), (rx+TILE, ry), 1)
    pygame.draw.line(surf, C_BLACK, (rx, ry), (rx, ry+TILE), 1)


def _draw_water(surf, rx, ry, tick):
    pygame.draw.rect(surf, C_WATER, (rx, ry, TILE, TILE))
    wave_off = int(8 * ((tick // 20 + rx) % 2 == 0))
    pygame.draw.ellipse(surf, C_WATER2,
                        (rx+4, ry+8+wave_off, TILE-8, 8))
    pygame.draw.ellipse(surf, C_WATER2,
                        (rx+6, ry+26-wave_off, TILE-12, 6))


def build_tile_cache(tick=0):
    cache = {}
    for tid in (T_GRASS, T_WALL, T_WATER, T_SAND, T_DIRT, T_DOOR):
        s = pygame.Surface((TILE, TILE))
        if tid == T_GRASS:
            s.fill(C_GRASS)
            for bx, by in ((6,6),(20,18),(36,10),(10,34),(30,30)):
                pygame.draw.rect(s, C_GRASS2, (bx, by, 4, 4))
        elif tid == T_WALL:
            _draw_wall(s, 0, 0)
        elif tid == T_WATER:
            _draw_water(s, 0, 0, tick)
        elif tid == T_SAND:
            s.fill(C_SAND)
            for bx, by in ((8,8),(24,20),(38,36)):
                pygame.draw.circle(s, C_DIRT, (bx, by), 3)
        elif tid == T_DIRT:
            s.fill(C_DIRT)
        elif tid == T_DOOR:
            s.fill(C_WALL)
            pygame.draw.rect(s, C_DOOR, (10, 10, TILE-20, TILE-10))
            pygame.draw.circle(s, C_WALL_LT, (TILE//2, TILE//2), 4)
        cache[tid] = s
    return cache


class TileMap:
    def __init__(self):
        self.data = WORLD_MAP
        self.cols = MAP_COLS
        self.rows = MAP_ROWS
        self.tick = 0
        self._water_cache = {}

    def tile_at(self, col, row):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        return T_WALL

    def is_solid(self, col, row):
        return self.tile_at(col, row) in SOLID

    def rect_blocked(self, rect, solid=None):
        """True if any corner of rect overlaps a tile in *solid* (defaults to SOLID)."""
        if solid is None:
            solid = SOLID
        margin = 2
        for cx, cy in (
            (rect.left + margin, rect.top + margin),
            (rect.right - margin, rect.top + margin),
            (rect.left + margin, rect.bottom - margin),
            (rect.right - margin, rect.bottom - margin),
        ):
            if self.tile_at(int(cx // TILE), int(cy // TILE)) in solid:
                return True
        return False

    def draw(self, surf, camera):
        self.tick += 1
        cam_x, cam_y = camera

        # visible tile range
        col0 = max(0, int(cam_x // TILE))
        row0 = max(0, int(cam_y // TILE))
        col1 = min(self.cols, col0 + SCREEN_W // TILE + 2)
        row1 = min(self.rows, row0 + SCREEN_H // TILE + 2)

        for row in range(row0, row1):
            for col in range(col0, col1):
                tid = self.data[row][col]
                rx = col * TILE - cam_x
                ry = row * TILE - cam_y

                if tid == T_GRASS:
                    pygame.draw.rect(surf, C_GRASS, (rx, ry, TILE, TILE))
                    if (col + row) % 3 == 0:
                        pygame.draw.rect(surf, C_GRASS2, (rx+4, ry+4, 6, 6))
                elif tid == T_WALL:
                    _draw_wall(surf, rx, ry)
                elif tid == T_WATER:
                    _draw_water(surf, rx, ry, self.tick)
                elif tid == T_SAND:
                    pygame.draw.rect(surf, C_SAND, (rx, ry, TILE, TILE))
                    if (col * 3 + row) % 5 == 0:
                        pygame.draw.circle(surf, C_DIRT, (rx+16, ry+16), 3)
                elif tid == T_DIRT:
                    pygame.draw.rect(surf, C_DIRT, (rx, ry, TILE, TILE))
                elif tid == T_DOOR:
                    pygame.draw.rect(surf, C_WALL, (rx, ry, TILE, TILE))
                    pygame.draw.rect(surf, C_DOOR,
                                     (rx+10, ry+10, TILE-20, TILE-10))
                    pygame.draw.circle(surf, C_WALL_LT,
                                       (rx+HALF_TILE, ry+HALF_TILE), 4)
