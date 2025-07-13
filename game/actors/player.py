import random

import pygame

from game.utils.config import ORANGE, RED, SCREEN_HEIGHT, SCREEN_WIDTH, YELLOW_GREEN


class Player:
    """プレイヤークラス"""

    def __init__(self, images=None):
        """初期化関数"""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = 40
        self.height = 30
        self.speed = 5
        self.life = 3
        self.alive = True
        self.shot_count = 1
        self.images = images
        self.hit_timer = 0  # ヒット後の無敵時間タイマー
        self.invincible_duration = 60  # 無敵時間の長さ
        self.color = YELLOW_GREEN  # デフォルト色
        if random.random() < 0.01:  # 1%の確率でオレンジ色にするロジック
            self.color = ORANGE

    def move_left(self):
        """左に移動する関数"""
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        """右に移動する関数"""
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def update(self):
        """プレイヤーを更新する関数"""
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def draw(self, screen):
        """プレイヤーを画面に描画する関数"""
        if self.alive:
            draw_color = self.color
            if self.hit_timer > 0:  # 無敵時間中なら点滅させる
                if (self.hit_timer // 5) % 2 == 0:  # 5フレームごとに色を切り替え
                    draw_color = RED  # 赤く点滅
                else:
                    draw_color = self.color  # 通常色
            pygame.draw.rect(screen, draw_color, (self.x, self.y + 10, self.width, 10))
            pygame.draw.rect(
                screen, draw_color, (self.x + self.width // 2 - 5, self.y, 10, 10)
            )
            pygame.draw.rect(screen, draw_color, (self.x + 5, self.y + 20, 5, 10))
            pygame.draw.rect(
                screen, draw_color, (self.x + self.width - 10, self.y + 20, 5, 10)
            )

    def draw_life(self, screen):
        """残りライフを画面に描画する関数"""
        for i in range(self.life):
            screen.blit(self.images["heart"], (10 + i * 35, 5))
