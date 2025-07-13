import pygame
from player import Player
from enemy import Enemy
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.enemy import Enemy


class Bullet:
    def __init__(self, x, y, speed_y, color, speed_x=0):
        self.x = float(x)
        self.y = float(y)
        self.width = 5
        self.height = 10
        self.speed_y = speed_y
        self.speed_x = float(speed_x)
        self.color = color
        self.active = True

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        if self.y < 0 or self.y > SCREEN_HEIGHT or self.x < 0 or self.x > SCREEN_WIDTH:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(
                screen, self.color, (int(self.x), int(self.y), self.width, self.height)
            )

    def check_collision(self, target):
        if self.active and hasattr(target, "alive") and target.alive:
            if (
                self.x < target.x + target.width
                and self.x + self.width > target.x
                and self.y < target.y + target.height
                and self.y + self.height > target.y
            ):
                self.active = False
<<<<<<< HEAD:game/bullet.py
                if isinstance(target, Player):
                    target.alive = False
=======
                if isinstance(target, Enemy):
                    target.alive = False

>>>>>>> f05705fc81e46f00c2e2a576b38adc0072b60aa5:game/game_bullet.py
                return True
        return False
