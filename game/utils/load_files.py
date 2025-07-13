import pygame

from game.utils.config import BLACK, BLUE, LIGHTBLUE, ORANGE, RED, YELLOW


def load_image(path, size, fallback_color):
    """画像を読み込み、サイズを変更する。"""
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except pygame.error:
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface


def load_images():
    """ゲームで使用する画像をロードする。"""
    enemy1_img = load_image("game/resources/images/enemy1.png", (40, 30), RED)
    enemy2_img = load_image("game/resources/images/enemy2.png", (40, 30), ORANGE)
    enemy3_img = load_image("game/resources/images/enemy3.png", (45, 35), LIGHTBLUE)
    heart_img = load_image("game/resources/images/heart.png", (30, 30), RED)
    item_shot_img = load_image("game/resources/images/shot.png", (25, 25), BLUE)
    item_sub_shot_img = load_image(
        "game/resources/images/sub_shot.png", (25, 25), YELLOW
    )
    item_score_x2_img = load_image("game/resources/images/2.png", (25, 25), BLACK)

    return {
        "enemy1": enemy1_img,
        "enemy2": enemy2_img,
        "enemy3": enemy3_img,
        "heart": heart_img,
        "item_shot": item_shot_img,
        "item_sub_shot": item_sub_shot_img,
        "item_score_x2": item_score_x2_img,
    }


def load_sound(sound_path):
    """サウンドファイルをロードする。"""
    try:
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(0.25)
        return sound
    except pygame.error:
        print(f"{sound_path} が見つかりませんでした。サウンドは再生されません。")
        return None


def load_sounds():
    """ゲームで使用するサウンドをロードする。"""
    player_hit_sound = load_sound("game/resources/sounds/break.mp3")
    game_over_hit_sound = load_sound("game/resources/sounds/break_last.mp3")

    return {
        "player_hit": player_hit_sound,
        "game_over_hit": game_over_hit_sound,
    }
