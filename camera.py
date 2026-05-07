from settings import SCREEN_W, SCREEN_H
from tilemap import MAP_PX_W, MAP_PX_H


class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def update(self, target_rect):
        tx = target_rect.centerx - SCREEN_W // 2
        ty = target_rect.centery - SCREEN_H // 2
        # clamp to world bounds
        self.x = max(0, min(tx, MAP_PX_W - SCREEN_W))
        self.y = max(0, min(ty, MAP_PX_H - SCREEN_H))

    def apply(self, rect):
        return rect.move(-int(self.x), -int(self.y))

    @property
    def offset(self):
        return (int(self.x), int(self.y))
