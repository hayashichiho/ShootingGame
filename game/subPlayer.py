import pygame
from bullet import Bullet
from config import WHITE, YELLOW_GREEN


# サブ機体クラス
class SubPlayer:
    def __init__(self, player_ref, side_offset):
        self.player_ref = player_ref
        self.width = 30
        self.height = 20
        self.offset_y = 30
        self.side_offset = side_offset
        self.shoot_interval = 90
        self.shoot_timer = self.shoot_interval
        self.alive = True

    def update(self):
        self.x = (
            self.player_ref.x
            + (self.player_ref.width // 2)
            + (self.side_offset * (self.player_ref.width // 2 + 10))
            - (self.width // 2)
        )
        self.y = self.player_ref.y - self.offset_y

        self.shoot_timer -= 1
        bullets_fired = []
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_interval
            bullets_fired.append(
                Bullet(self.x + self.width // 2 - 2, self.y, -7, WHITE, 0)
            )
        return bullets_fired

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW_GREEN, (self.x, self.y + 10, self.width, 10))
        pygame.draw.rect(
            screen, YELLOW_GREEN, (self.x + self.width // 2 - 5, self.y, 10, 10)
        )
