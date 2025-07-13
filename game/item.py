from config import SCREEN_HEIGHT
from images import (
    item_score_x2_img,
    item_shot_img,
    item_sub_shot_img,
)


# アイテムクラス
class Item:
    def __init__(self, x, y, item_type="shot_up"):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = 2
        self.active = True
        self.item_type = item_type

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        if self.active:
            if self.item_type == "shot_up":
                screen.blit(item_shot_img, (self.x, self.y))
            elif self.item_type == "sub_shot_up":
                screen.blit(item_sub_shot_img, (self.x, self.y))
            elif self.item_type == "score_x2":
                screen.blit(item_score_x2_img, (self.x, self.y))

    def check_collision(self, player):
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
