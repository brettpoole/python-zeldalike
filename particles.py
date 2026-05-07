import pygame
import random


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "radius")

    def __init__(self, x, y, color, count=6, speed=2.5, life=20):
        self.x = x
        self.y = y
        self.vx = random.uniform(-speed, speed)
        self.vy = random.uniform(-speed, speed)
        self.life = life + random.randint(-4, 4)
        self.max_life = self.life
        self.color = color
        self.radius = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.life -= 1

    def draw(self, surf, cam_x, cam_y):
        alpha = self.life / self.max_life
        r = int(self.color[0] * alpha)
        g = int(self.color[1] * alpha)
        b = int(self.color[2] * alpha)
        rad = max(1, int(self.radius * alpha))
        pygame.draw.circle(surf, (r, g, b),
                           (int(self.x - cam_x), int(self.y - cam_y)), rad)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, color, count=8, speed=2.5, life=22):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed=speed, life=life))

    def update(self):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

    def draw(self, surf, cam_x, cam_y):
        for p in self.particles:
            p.draw(surf, cam_x, cam_y)


class FloatingText:
    __slots__ = ("x", "y", "text", "color", "life", "max_life", "font")

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
        alpha = min(255, int(255 * self.life / self.max_life))
        img = self.font.render(self.text, True, self.color)
        img.set_alpha(alpha)
        surf.blit(img, (int(self.x - cam_x) - img.get_width() // 2,
                        int(self.y - cam_y)))
