import sys

import pygame

# Pygameの初期化
pygame.init()

# 画面サイズの設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("シンプルインベーダーゲーム")

# 色の定義
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW_GREEN = (154, 205, 50)
WHITE = (255, 255, 255)


# プレイヤークラス
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = 50
        self.height = 30
        self.speed = 5

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(
            screen, YELLOW_GREEN, (self.x, self.y, self.width, self.height)
        )


# 敵クラス
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.alive = True

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))


# 弾クラス
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 7
        self.active = True

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def check_collision(self, enemy):
        if (
            self.active
            and enemy.alive
            and self.x < enemy.x + enemy.width
            and self.x + self.width > enemy.x
            and self.y < enemy.y + enemy.height
            and self.y + self.height > enemy.y
        ):
            self.active = False
            enemy.alive = False
            return True
        return False


# ゲームのメインクラス
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.clock = pygame.time.Clock()

        # 敵を5体配置
        for i in range(5):
            enemy = Enemy(150 + i * 100, 100)
            self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 弾を発射
                    bullet = Bullet(
                        self.player.x + self.player.width // 2 - 2, self.player.y
                    )
                    self.bullets.append(bullet)

        # キーの押し続け判定
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

        return True

    def update(self):
        # 弾の更新
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
            else:
                # 衝突判定
                for enemy in self.enemies:
                    bullet.check_collision(enemy)

    def draw(self):
        # 背景を黒で塗りつぶし
        screen.fill(BLACK)

        # プレイヤーを描画
        self.player.draw(screen)

        # 敵を描画
        for enemy in self.enemies:
            enemy.draw(screen)

        # 弾を描画
        for bullet in self.bullets:
            bullet.draw(screen)

        # 画面更新
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60FPS

        pygame.quit()
        sys.exit()


# ゲームの実行
if __name__ == "__main__":
    game = Game()
    game.run()
