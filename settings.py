SCREEN_W = 960
SCREEN_H = 640
FPS = 60
TITLE = "Dungeons of Eld"

TILE = 48          # pixels per tile
HALF_TILE = TILE // 2

MAP_COLS  = 42
MAP_ROWS  = 22
MAP_PX_W  = MAP_COLS * TILE
MAP_PX_H  = MAP_ROWS * TILE

# Colours
C_BLACK   = (0, 0, 0)
C_WHITE   = (255, 255, 255)
C_GRASS   = (72, 140, 56)
C_GRASS2  = (64, 128, 48)
C_DIRT    = (160, 120, 72)
C_WALL    = (90, 80, 70)
C_WALL_LT = (120, 108, 92)
C_WATER   = (60, 120, 200)
C_WATER2  = (80, 140, 220)
C_SAND    = (210, 190, 130)
C_DOOR    = (180, 140, 60)

C_PLAYER  = (60, 120, 220)
C_PLAYER_LT = (120, 170, 255)
C_SWORD   = (220, 220, 100)

C_SLIME   = (80, 200, 80)
C_SLIME_DK = (40, 150, 40)
C_SKULL   = (200, 60, 60)
C_SKULL_DK = (140, 30, 30)
C_BAT     = (160, 80, 200)
C_BAT_DK  = (110, 40, 160)

C_HEART_FULL = (220, 60, 60)
C_HEART_EMPTY = (80, 40, 40)
C_XP_BAR  = (80, 200, 255)
C_HUD_BG  = (20, 20, 30, 200)

C_DMG     = (255, 80, 80)
C_HEAL    = (80, 255, 120)

PLAYER_SPEED  = 3
PLAYER_MAX_HP = 6       # half-hearts → 3 full hearts
SWORD_DAMAGE  = 1
SWORD_FRAMES  = 3      # frames the sword hitbox is active
SWORD_COOLDOWN = 8     # frames between attacks
I_FRAMES      = 45      # invincibility frames after taking damage

SLIME_SPEED   = 1.2
SLIME_HP      = 1
SLIME_DAMAGE  = 1
SLIME_XP      = 10

SKULL_SPEED   = 1.6
SKULL_HP      = 5
SKULL_DAMAGE  = 2
SKULL_XP      = 20

BAT_SPEED     = 2.2
BAT_HP        = 2
BAT_DAMAGE    = 1
BAT_XP        = 15

XP_PER_LEVEL  = 50
