import random

import pygame

from config import ORANGE, RED, LIGHTBLUE, SCREEN_WIDTH

# 画像の読み込み
try:
    enemy1_img = pygame.image.load("game/images/enemy1.png")
    enemy1_img = pygame.transform.scale(enemy1_img, (40, 30))
except pygame.error:
    enemy1_img = pygame.Surface((40, 30))
    enemy1_img.fill(RED)

try:
    enemy2_img = pygame.image.load("game/images/enemy2.png")
    enemy2_img = pygame.transform.scale(enemy2_img, (40, 30))
except pygame.error:
    enemy2_img = pygame.Surface((40, 30))
    enemy2_img.fill(ORANGE)

try:
    enemy3_img = pygame.image.load("game/images/enemy3.png")
    enemy3_img = pygame.transform.scale(enemy3_img, (45, 35))
except pygame.error:
    enemy3_img = pygame.Surface((45, 35))
    enemy3_img.fill(LIGHTBLUE)


class Enemy:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.alive = True
        self.type_id = type_id
        self.speed_y = 1
        self.speed_x = 2 if type_id == 1 else 0
        self.direction = 1
        self.shoot_timer = random.randint(90, 180)

        if self.type_id == 2:
            self.hp = 3
        else:
            self.hp = 1

    def update(self):
        self.y += self.speed_y
        if self.type_id == 1:
            self.x += self.speed_x * self.direction
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
                self.direction *= -1
        self.shoot_timer -= 1

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    def should_shoot(self):
        return self.shoot_timer <= 0

    def reset_shoot_timer(self):
        self.shoot_timer = random.randint(100, 200)

    def draw(self, screen):
        if self.alive:
          if self.type_id == 0:
             screen.blit(enemy1_img, (self.x, self.y))
          elif self.type_id == 1:
             screen.blit(enemy2_img, (self.x, self.y))
          elif self.type_id == 2:
             screen.blit(enemy3_img, (self.x, self.y))
