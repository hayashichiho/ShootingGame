import sys

import pygame
import requests

from game.core.game_core import GameCore
from game.core.game_ui import GameUI
from game.utils.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.utils.load_files import load_images, load_sounds


def run(ui):
    """ゲームのメインループ"""
    running = True
    while running:
        running = ui.handle_events()
        if not ui.core.game_over:
            ui.core.update()
            ui.draw()
        else:
            ui.draw()
            save_score_to_server(ui)
            pygame.time.wait(3000)
            running = False
        ui.clock.tick(60)
    pygame.quit()
    sys.exit()


def save_score_to_server(ui):
    """スコアをサーバーに送信"""
    try:
        print(f"\nゲームオーバー! 最終スコア: {ui.core.score}")
        data = {"player_name": ui.core.player_name, "score": ui.core.score}
        response = requests.post(
            "http://localhost:5000/api/save-score", json=data, timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("スコアがランキングに保存されました！")
            else:
                print(f"スコア保存失敗: {result.get('message')}")
        else:
            print(f"サーバーエラー: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"ネットワークエラー: {e}")
    except Exception as e:
        print(f"スコア保存エラー: {e}")


def main():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.init()
    pygame.mixer.set_num_channels(16)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SHOOTING GAME")
    images = load_images()
    sounds = load_sounds()
    player_name = sys.argv[1] if len(sys.argv) > 1 else "Player1"
    core = GameCore(images, sounds, player_name)
    ui = GameUI(core, screen)
    run(ui)


if __name__ == "__main__":
    main()
