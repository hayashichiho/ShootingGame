import pygame
from config import BLACK, BLUE, ORANGE, RED, YELLOW


def load_image(path, size, fallback_color):
    """画像を読み込み、失敗した場合は指定色のSurfaceを返す"""
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except pygame.error:
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface


# 画像の読み込み
enemy1_img = load_image("game/images/enemy1.png", (40, 30), RED)
enemy2_img = load_image("game/images/enemy2.png", (40, 30), ORANGE)
enemy3_img = load_image("game/images/enemy2.png", (45, 35), LIGHTBLUE)
item_shot_img = load_image("game/items/shot.png", (25, 25), BLUE)
item_sub_shot_img = load_image("game/items/sub_shot.png", (25, 25), YELLOW)
item_score_x2_img = load_image("game/items/2.png", (25, 25), BLACK)
heart_img = load_image("game/images/heart.png", (30, 30), RED)
