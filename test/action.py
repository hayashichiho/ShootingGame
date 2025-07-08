import pygame
import sys
import random

pygame.init()

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("インベーダーゲーム")

# 色の定義
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW_GREEN = (154, 205, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# プレイヤークラス
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = 40
        self.height = 30
        self.speed = 5
        self.alive = True
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x, self.y + 10, self.width, 10)) 
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x + self.width // 2 - 5, self.y, 10, 10))
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x + 5, self.y + 20, 5, 10))
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x + self.width - 10, self.y + 20, 5, 10))

# 弾クラス
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

    def check_collision(self, target):
        if self.active and target.alive:
            if (self.x < target.x + target.width and
                self.x + self.width > target.x and
                self.y < target.y + target.height and
                self.y + self.height > target.y):
                self.active = False
                if isinstance(target, Player):
                    target.alive = False
                elif isinstance(target, Enemy):
                    target.alive = False
                return True
        return False

# 画像の読み込み（ダミーファイル対応）
try:
    enemy1_img = pygame.image.load("enemy1.png")
    enemy1_img = pygame.transform.scale(enemy1_img, (40, 30))
except pygame.error:
    enemy1_img = pygame.Surface((40, 30))
    enemy1_img.fill(RED)

try:
    enemy2_img = pygame.image.load("enemy2.png")
    enemy2_img = pygame.transform.scale(enemy2_img, (40, 30))
except pygame.error:
    enemy2_img = pygame.Surface((40, 30))
    enemy2_img.fill(ORANGE)

# 敵クラス
class Enemy:
    def __init__(self, x, y, type_id):
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
        
    def update(self):
        self.y += self.speed_y
        if self.type_id == 1:
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
            if self.type_id == 0:
                screen.blit(enemy1_img, (self.x, self.y))
            else:
                screen.blit(enemy2_img, (self.x, self.y))

# ゲームのメインクラス
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.clock = pygame.time.Clock()
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False
        
        self.next_enemy_add_score = 200 
        self.next_speed_increase_score = 1000 

        self.initial_spawn_interval = 60 
        self.current_spawn_interval = self.initial_spawn_interval
        self.spawn_interval_decrease_threshold = 500 
        self.spawn_decrease_amount = 5 

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
                if not self.game_over and event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player.x + self.player.width // 2 - 2, self.player.y, -7, WHITE)
                    self.player_bullets.append(bullet)

        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()

        return True

    def update(self):
        if self.game_over:
            return

        for bullet in self.player_bullets[:]:
            bullet.update()
            if not bullet.active:
                self.player_bullets.remove(bullet)
            else:
                for enemy in self.enemies:
                    if bullet.check_collision(enemy):
                        self.score += 100
                        break

        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if not bullet.active:
                self.enemy_bullets.remove(bullet)
            elif bullet.check_collision(self.player):
                print("プレイヤーに命中！ゲームオーバー！")
                self.game_over = True
                break

        for enemy in self.enemies:
            if enemy.alive:
                enemy.update()
                if (enemy.x < self.player.x + self.player.width and
                    enemy.x + enemy.width > self.player.x and
                    enemy.y < self.player.y + self.player.height and
                    enemy.y + enemy.height > self.player.y):
                    self.player.alive = False
                    self.game_over = True
                    print("敵がプレイヤーに接触！ゲームオーバー！")
                    break

                if enemy.should_shoot():
                    bullet = Bullet(enemy.x + enemy.width // 2, enemy.y + enemy.height, 4, YELLOW)
                    self.enemy_bullets.append(bullet)
                    enemy.reset_shoot_timer()

        if self.score >= self.spawn_interval_decrease_threshold and self.current_spawn_interval > 10:
            self.current_spawn_interval = max(10, self.current_spawn_interval - self.spawn_decrease_amount)
            self.spawn_interval_decrease_threshold += 500

        self.spawn_timer += 1
        if self.spawn_timer >= self.current_spawn_interval:
            type_id = random.choice([0, 1])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -30, type_id)
            self.enemies.append(enemy)
            self.spawn_timer = 0

        while self.score >= self.next_enemy_add_score:
            type_id = random.choice([0, 1])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -random.randint(50, 200), type_id) 
            self.enemies.append(enemy)
            self.next_enemy_add_score += 200 
            print(f"スコア {self.score} で新しい敵を追加。現在の敵数: {len(self.enemies)}")

        while self.score >= self.next_speed_increase_score:
            for enemy in self.enemies:
                enemy.speed_y *= 1.1 
                enemy.speed_x *= 1.1
            self.next_speed_increase_score += 1000 
            print(f"スコア {self.score} で敵の速度が上昇。")

        self.enemies = [enemy for enemy in self.enemies if enemy.alive and enemy.y < SCREEN_HEIGHT]

        if not self.player.alive: 
            self.game_over = True

    def draw(self):
        screen.fill(BLACK)

        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.draw(screen)

        score_font = pygame.font.Font(None, 36)
        score_text = f"SCORE: {self.score}"
        score_surface = score_font.render(score_text, True, WHITE)

        if self.game_over:
            font_large = pygame.font.Font(None, 74)
            game_over_text = font_large.render("GAME OVER", True, RED)
            rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, rect)

            score_font_game_over = pygame.font.Font(None, 50) 
            score_surface_game_over = score_font_game_over.render(score_text, True, WHITE)
            score_rect_game_over = score_surface_game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)) 
            screen.blit(score_surface_game_over, score_rect_game_over)
        else:
            screen.blit(score_surface, (10, 10))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

            if self.game_over:
                pygame.time.wait(3000)
                running = False

        pygame.quit()
        sys.exit()

# ゲームの実行
if __name__ == "__main__":
    Game().run()