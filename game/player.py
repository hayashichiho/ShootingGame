import pygame
import random
from config import SCREEN_HEIGHT, SCREEN_WIDTH, YELLOW_GREEN,RED,ORANGE
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
        self.hit_timer = 0 # ヒット後の無敵時間タイマー
        self.invincible_duration = 60 # 無敵時間の長さ
        self.color = YELLOW_GREEN # デフォルト色
        if random.random()<0.01: # 1%の確率でオレンジ色にするロジック
            self.color = ORANGE

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def update(self): # プレイヤーの更新メソッドを追加
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def draw(self, screen):
        if self.alive:
            draw_color = self.color
            if self.hit_timer > 0: # 無敵時間中なら点滅させる
                if (self.hit_timer // 5) % 2 == 0: # 5フレームごとに色を切り替え
                    draw_color =  RED # 赤く点滅
                else:
                    draw_color = self.color # 通常色
            pygame.draw.rect(
                screen, draw_color, (self.x, self.y + 10, self.width, 10)
            )
            pygame.draw.rect(
                screen, draw_color, (self.x + self.width // 2 - 5, self.y, 10, 10)
            )
            pygame.draw.rect(screen, draw_color, (self.x + 5, self.y + 20, 5, 10))
            pygame.draw.rect(
                screen, draw_color, (self.x + self.width - 10, self.y + 20, 5, 10)
            )

    def draw_life(self, screen):
        for i in range(self.life):
            screen.blit(heart_img, (10 + i * 35, 5))
