import pygame

from game.actors.bullet import Bullet

from ..utils.config import BLACK, RED, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE


class GameUI:
    """ゲームのUIクラス"""

    def __init__(self, core, screen):
        """初期化関数"""
        self.core = core
        self.screen = screen
        self.clock = pygame.time.Clock()

    def handle_events(self):
        """イベントを処理する関数"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.core.game_over:
                    pass
                elif event.key == pygame.K_SPACE and self.core.player.alive:
                    # プレイヤーのショットを発射
                    for i in range(self.core.player.shot_count):
                        offset = (
                            i - (self.core.player.shot_count - 1) / 2
                        ) * 20  # ショットの間隔
                        diagonal_speed_factor = 1.5  # 斜めの弾速調整
                        bullet_speed_x = (
                            i - (self.core.player.shot_count - 1) / 2
                        ) * diagonal_speed_factor

                        bullet = Bullet(
                            self.core.player.x
                            + self.core.player.width // 2
                            - 2
                            + offset,
                            self.core.player.y,
                            -7,
                            WHITE,
                            bullet_speed_x,
                        )
                        self.core.player_bullets.append(bullet)

        # プレイヤーの移動処理
        keys = pygame.key.get_pressed()
        if not self.core.game_over:
            if keys[pygame.K_LEFT]:
                self.core.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.core.player.move_right()
        return True

    def draw(self):
        """画面を描画する関数"""
        self.screen.fill(BLACK)

        # プレイヤーと敵，弾，アイテムの描画
        self.core.player.draw(self.screen)
        self.core.player.draw_life(self.screen)
        for enemy in self.core.enemies:
            enemy.draw(self.screen)
        for bullet in self.core.player_bullets + self.core.enemy_bullets:
            bullet.draw(self.screen)
        for item in self.core.items:
            item.draw(self.screen)
        for sub_player in self.core.sub_players:
            sub_player.draw(self.screen)

        # スコア表示
        score_font = pygame.font.Font(None, 36)
        score_text = f"SCORE: {self.core.score}"
        score_surface = score_font.render(score_text, True, WHITE)

        # ゲームオーバー時の表示
        if self.core.game_over:
            font_large = pygame.font.Font(None, 74)
            game_over_text = font_large.render("GAME OVER", True, RED)
            rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(game_over_text, rect)

            score_font_game_over = pygame.font.Font(None, 50)
            score_surface_game_over = score_font_game_over.render(
                score_text, True, WHITE
            )
            score_rect_game_over = score_surface_game_over.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
            )
            self.screen.blit(score_surface_game_over, score_rect_game_over)
        else:
            score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
            self.screen.blit(score_surface, score_rect)

        pygame.display.flip()
