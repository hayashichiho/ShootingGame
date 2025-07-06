import pygame
import sys
import random 

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
        self.width = 40 # 形状に合わせて幅を調整
        self.height = 20 # 胴体部分の高さ
        self.speed = 5
        self.alive = True # プレイヤーの生存状態
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            
    def draw(self, screen):
        if self.alive: # プレイヤーが生きている場合のみ描画
            # 自機の形状をピクセルアート風に描画
            # 胴体部分
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x, self.y + 10, self.width, 10)) 
            # 中央のコックピット部分
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x + self.width // 2 - 5, self.y, 10, 10))
            # 左右の脚部
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x + 5, self.y + 20, 5, 10))
            pygame.draw.rect(screen, YELLOW_GREEN, (self.x + self.width - 10, self.y + 20, 5, 10))


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

    def shoot_bullet(self):
        return None

# 弾クラス
class Bullet:
    def __init__(self, x, y): 
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 7 
        self.active = True
        self.color = WHITE 
        
    def update(self):
        self.y -= self.speed
        if self.y < 0: 
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

# ゲームのメインクラス
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.bullets = [] 
        self.clock = pygame.time.Clock()
        self.score = 0
        self.game_over = False 

        self.next_enemy_spawn_threshold = 200 # 次の敵を生成するスコアの閾値
        
        # 敵を5体配置
        for i in range(5):
            enemy = Enemy(150 + i * 100, 100)
            self.enemies.append(enemy)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # ゲームオーバー中は操作不可
                if not self.game_over:
                    if event.key == pygame.K_SPACE:
                        # 弾の発射位置を自機の形状に合わせて調整
                        bullet = Bullet(self.player.x + self.player.width // 2 - 2, self.player.y) 
                        self.bullets.append(bullet)
                    
        # キーの押し続け判定
        keys = pygame.key.get_pressed()
        # ゲームオーバー中は操作不可
        if not self.game_over:
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()
            
        return True
        
    def update(self):
        # ゲームオーバーなら更新処理をスキップ
        if self.game_over:
            return

        # プレイヤーの弾の更新
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
            else:
                for enemy in self.enemies:
                    if bullet.check_collision(enemy):
                        self.score += 100 
                        break 

        # スコアが200の倍数になったら敵を増やす
        while self.score >= self.next_enemy_spawn_threshold:
            new_enemy_x = random.randint(0, SCREEN_WIDTH - Enemy(0,0).width)
            new_enemy_y = 50 
            self.enemies.append(Enemy(new_enemy_x, new_enemy_y))
            print(f"スコア {self.score} で新しい敵を生成しました。現在の敵の数: {len(self.enemies)}")
            self.next_enemy_spawn_threshold += 200

        # 敵がプレイヤーの位置まで到達した場合のゲームオーバー判定
        for enemy in self.enemies:
            if enemy.alive and enemy.y + enemy.height > self.player.y: 
                self.game_over = True
                print("敵がプレイヤーに到達！ゲームオーバー！")
                break 

        self.enemies = [enemy for enemy in self.enemies if enemy.alive]

        # ゲームオーバー判定（プレイヤーが死ぬ条件は敵の弾がないため実質発生しない）
        if not self.player.alive: 
            self.game_over = True
            
    def draw(self):
        screen.fill(BLACK)
        
        self.player.draw(screen)
        
        for enemy in self.enemies:
            enemy.draw(screen)
            
        for bullet in self.bullets: 
            bullet.draw(screen)

        # スコア表示
        score_font = pygame.font.Font(None, 36)
        score_text = f"SCORE: {self.score}"
        score_surface = score_font.render(score_text, True, WHITE)
            
        # ゲームオーバーのメッセージを表示
        if self.game_over:
            font_large = pygame.font.Font(None, 74)
            game_over_text = font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect)

            # ゲームオーバー時にスコアを中央に表示
            score_font_game_over = pygame.font.Font(None, 50) 
            score_surface_game_over = score_font_game_over.render(score_text, True, WHITE)
            score_rect_game_over = score_surface_game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)) 
            screen.blit(score_surface_game_over, score_rect_game_over)
        else:
            # ゲーム中はスコアを左上に表示
            screen.blit(score_surface, (10, 10))
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  
            
            # ゲームオーバーになったら3秒待って終了
            if self.game_over:
                pygame.time.wait(3000) 
                running = False 

        pygame.quit()
        sys.exit()

# ゲームの実行
if __name__ == "__main__":
    game = Game()
    game.run()