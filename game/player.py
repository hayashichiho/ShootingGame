import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, YELLOW_GREEN
from images import heart_img


# プレイヤークラス
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = 40
        self.height = 30
        self.speed = 5
        self.life = 3
        self.alive = True
        self.shot_count = 1

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(
                screen, YELLOW_GREEN, (self.x, self.y + 10, self.width, 10)
            )
            pygame.draw.rect(
                screen, YELLOW_GREEN, (self.x + self.width // 2 - 5, self.y, 10, 10)
            )
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x + 5, self.y + 20, 5, 10))
            pygame.draw.rect(
                screen, YELLOW_GREEN, (self.x + self.width - 10, self.y + 20, 5, 10)
            )

    def draw_life(self, screen):
        for i in range(self.life):
            screen.blit(heart_img, (10 + i * 35, 5))
