import pygame

from game.utils.config import (  # SCREEN_WIDTH, SCREEN_HEIGHTのインポート
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Bullet:
    """弾クラス"""

    def __init__(self, x, y, speed_y, color, speed_x=0):
        """初期化関数"""
        self.x = float(x)
        self.y = float(y)
        self.width = 5
        self.height = 10
        self.speed_y = speed_y
        self.speed_x = float(speed_x)
        self.color = color
        self.active = True

    def update(self):
        """弾を更新する関数"""
        self.y += self.speed_y
        self.x += self.speed_x
        if self.y < 0 or self.y > SCREEN_HEIGHT or self.x < 0 or self.x > SCREEN_WIDTH:
            self.active = False

    def draw(self, screen):
        """弾を画面に描画する関数"""
        if self.active:
            pygame.draw.rect(
                screen, self.color, (int(self.x), int(self.y), self.width, self.height)
            )

    def check_collision(self, target):
        """ターゲットとの衝突をチェックする関数"""
        if self.active and hasattr(target, "alive") and target.alive:
            if (
                self.x < target.x + target.width
                and self.x + self.width > target.x
                and self.y < target.y + target.height
                and self.y + self.height > target.y
            ):
                from game.actors.enemy import Enemy  # Enemyクラスのインポート
                from game.actors.player import Player  # Playerクラスのインポート

                self.active = False
                if isinstance(target, Player):
                    pass
                elif isinstance(target, Enemy):
                    target.take_damage()
                return True
        return False
