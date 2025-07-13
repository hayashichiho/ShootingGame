import random

from game.utils.config import SCREEN_WIDTH


class Enemy:
    """敵クラス"""

    def __init__(self, x, y, type_id, images):
        """初期化関数"""
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
        self.images = images

        if self.type_id == 2:
            self.hp = 3
        else:
            self.hp = 1

    def update(self):
        """敵を更新する関数"""
        self.y += self.speed_y
        if self.type_id == 1:
            self.x += self.speed_x * self.direction
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
                self.direction *= -1
        self.shoot_timer -= 1

    def take_damage(self):
        """敵がダメージを受ける関数"""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    def should_shoot(self):
        """敵が弾を撃つかどうかを判断する関数"""
        return self.shoot_timer <= 0

    def reset_shoot_timer(self):
        """弾を撃った後にタイマーをリセットする関数"""
        self.shoot_timer = random.randint(100, 200)

    def draw(self, screen):
        """敵を画面に描画する関数"""
        if self.alive:
            if self.type_id == 0:
                screen.blit(self.images["enemy1"], (self.x, self.y))
            elif self.type_id == 1:
                screen.blit(self.images["enemy2"], (self.x, self.y))
            elif self.type_id == 2:
                screen.blit(self.images["enemy3"], (self.x, self.y))
