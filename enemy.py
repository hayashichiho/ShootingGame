import pygame
import sys
import random

pygame.init()

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("インベーダーゲーム")

# 色
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW_GREEN = (154, 205, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# プレイヤー
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
        pygame.draw.rect(screen, YELLOW_GREEN, (self.x, self.y, self.width, self.height))
        point1 = (self.x + self.width // 2, self.y - 20)  # 三角の頂点（上）
        point2 = (self.x, self.y)                        # 左下
        point3 = (self.x + self.width, self.y)           # 右下
        pygame.draw.polygon(screen, YELLOW_GREEN, [point1, point2, point3])

# 弾
class Bullet:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = speed
        self.color = color
        self.active = True

    def update(self):
        self.y += self.speed
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, enemy):
        if (self.active and enemy.alive and
            self.x < enemy.x + enemy.width and
            self.x + self.width > enemy.x and
            self.y < enemy.y + enemy.height and
            self.y + self.height > enemy.y):
            self.active = False
            enemy.alive = False
            return True
        return False

# 敵（共通）
class Enemy:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.alive = True
        self.type_id = type_id  # 0: 直下降, 1: 斜め揺れ
        self.speed_y = 1
        self.speed_x = 2 if type_id == 1 else 0
        self.direction = 1
        self.shoot_timer = random.randint(90, 180)

    def update(self):
        self.y += self.speed_y
        if self.type_id == 1:  # 斜めに揺れるタイプ
            self.x += self.speed_x * self.direction
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
                self.direction *= -1
        self.shoot_timer -= 1

    def should_shoot(self):
        return self.shoot_timer <= 0

    def reset_shoot_timer(self):
        self.shoot_timer = random.randint(100, 200)

    def draw(self, screen):
        if self.alive:
            color = RED if self.type_id == 0 else ORANGE
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

# ゲーム本体
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.clock = pygame.time.Clock()
        self.spawn_timer = 0

        # 最初は3体だけ出す（ランダムなタイプ）
        for _ in range(3):
            type_id = random.choice([0, 1])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -random.randint(50, 300), type_id)
            self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player.x + self.player.width // 2 - 2, self.player.y, -7, WHITE)
                    self.player_bullets.append(bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

        return True

    def update(self):
        # プレイヤー弾
        for bullet in self.player_bullets[:]:
            bullet.update()
            if not bullet.active:
                self.player_bullets.remove(bullet)
            else:
                for enemy in self.enemies:
                    bullet.check_collision(enemy)

        # 敵弾
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if not bullet.active:
                self.enemy_bullets.remove(bullet)

        # 敵更新
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update()
                if enemy.should_shoot():
                    bullet = Bullet(enemy.x + enemy.width // 2, enemy.y + enemy.height, 4, YELLOW)
                    self.enemy_bullets.append(bullet)
                    enemy.reset_shoot_timer()

        # 敵追加（1秒に1体）
        self.spawn_timer += 1
        if self.spawn_timer >= 60:
            type_id = random.choice([0, 1])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -30, type_id)
            self.enemies.append(enemy)
            self.spawn_timer = 0

    def draw(self):
        screen.fill(BLACK)
        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.draw(screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# 実行
if __name__ == "__main__":
    Game().run()
