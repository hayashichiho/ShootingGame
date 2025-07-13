from game.utils.config import SCREEN_HEIGHT


class Item:
    """アイテムクラス"""

    def __init__(self, x, y, item_type="shot_up", images=None):
        """初期化関数"""
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = 2
        self.active = True
        self.item_type = item_type
        self.images = images

    def update(self):
        """アイテムを更新する関数"""
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        """アイテムを画面に描画する関数"""
        if self.active:
            if self.item_type == "shot_up":
                screen.blit(self.images["item_shot"], (self.x, self.y))
            elif self.item_type == "sub_shot_up":
                screen.blit(self.images["item_sub_shot"], (self.x, self.y))
            elif self.item_type == "score_x2":
                screen.blit(self.images["item_score_x2"], (self.x, self.y))

    def check_collision(self, player):
        """プレイヤーとの衝突をチェックする関数"""
        if self.active and player.alive:
            if (
                self.x < player.x + player.width
                and self.x + self.width > player.x
                and self.y < player.y + player.height
                and self.y + self.height > player.y
            ):
                self.active = False
                return True
        return False
