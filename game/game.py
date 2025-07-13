import pygame
import sys
import random
import requests

from config import (
    BLACK, RED, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, YELLOW, ORANGE, YELLOW_GREEN, BLUE, LIGHTBLUE,
)
from bullet import Bullet
from enemy import Enemy
from item import Item
from player import Player
from subPlayer import SubPlayer


pygame.init()

# 画面設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("インベーダーゲーム")

# ここから各種画像とサウンドの読み込み処理
try:
    enemy1_img = pygame.image.load("game/images/enemy1.png")
    enemy1_img = pygame.transform.scale(enemy1_img, (40, 30))
except pygame.error:
    enemy1_img = pygame.Surface((40, 30))
    enemy1_img.fill(RED)

try:
    enemy2_img = pygame.image.load("game/images/enemy2.png")
    enemy2_img = pygame.transform.scale(enemy2_img, (40, 30))
except pygame.error:
    enemy2_img = pygame.Surface((40, 30))
    enemy2_img.fill(ORANGE)

try:
    heart_img = pygame.image.load("game/images/heart.png")
    heart_img = pygame.transform.scale(heart_img, (30, 30))
except pygame.error:
    heart_img = pygame.Surface((30, 30))
    heart_img.fill(RED)

try:
    item_shot_img = pygame.image.load("game/items/shot.png")
    item_shot_img = pygame.transform.scale(item_shot_img, (25, 25))
except pygame.error:
    item_shot_img = pygame.Surface((25, 25))
    item_shot_img.fill(BLUE)

try:
    item_sub_shot_img = pygame.image.load("game/items/sub_shot.png")
    item_sub_shot_img = pygame.transform.scale(item_sub_shot_img, (25, 25))
except pygame.error:
    item_sub_shot_img = pygame.Surface((25, 25))
    item_sub_shot_img.fill(YELLOW) 

try:
    item_score_x2_img = pygame.image.load("game/items/2.png")
    item_score_x2_img = pygame.transform.scale(item_score_x2_img, (25, 25))
except pygame.error:
    item_score_x2_img = pygame.Surface((25, 25))
    item_score_x2_img.fill(BLACK)

# サウンドファイルのロード
player_hit_sound = None
game_over_hit_sound = None
try:
    player_hit_sound = pygame.mixer.Sound("game/sounds/break.mp3")
    player_hit_sound.set_volume(0.25) 
except pygame.error:
    print("game/sounds/break.mp3 が見つかりませんでした。通常のヒット音は再生されません。")

try:
    game_over_hit_sound = pygame.mixer.Sound("game/sounds/break_last.mp3")
    game_over_hit_sound.set_volume(0.25) 
except pygame.error:
    print("game/sounds/break_last.mp3 が見つかりませんでした。ゲームオーバー時のヒット音は再生されません。")


# ゲームのメインクラス
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock() 
        self.reset_game() 

    def reset_game(self):
        self.player = Player()
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.items = [] 
        self.sub_players = [] 
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False
        self.player_name = "Player1"

        self.next_enemy_add_score = 200 
        self.next_speed_increase_score = 1000 

        self.initial_spawn_interval = 60 
        self.current_spawn_interval = self.initial_spawn_interval
        self.spawn_interval_decrease_threshold = 500 
        self.spawn_decrease_amount = 5 

        self.score_multiplier = 1 
        self.score_multiplier_timer = 0 

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
                if self.game_over:
                    pass 
                elif event.key == pygame.K_SPACE and self.player.alive:
                    for i in range(self.player.shot_count):
                        offset = (i - (self.player.shot_count - 1) / 2) * 20 
                        diagonal_speed_factor = 1.5
                        bullet_speed_x = (i - (self.player.shot_count - 1) / 2) * diagonal_speed_factor
                        
                        bullet = Bullet(
                            self.player.x + self.player.width // 2 - 2 + offset, 
                            self.player.y, 
                            -7, 
                            WHITE, 
                            bullet_speed_x 
                        ) 
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
        
        self.player.update() 

        if self.score_multiplier_timer > 0:
            self.score_multiplier_timer -= 1
            if self.score_multiplier_timer == 0:
                self.score_multiplier = 1 
                print("スコア2倍効果が終了しました。")

        # **[変更開始] プレイヤー弾の更新と衝突判定を最適化**
        new_player_bullets = [] 
        for bullet in self.player_bullets:
            bullet.update()
            if bullet.active: 
                hit_enemy = False
                for enemy in self.enemies:
                    if bullet.check_collision(enemy): 
                        self.score += 100 * self.score_multiplier 
                        
                        rand_val = random.random()
                        
                        if rand_val < 0.10: 
                            item_to_drop = Item(enemy.x + enemy.width // 2 - 12, enemy.y + enemy.height // 2, "score_x2")
                            self.items.append(item_to_drop)
                        elif rand_val < 0.10 + 0.05: 
                            item_to_drop = Item(enemy.x + enemy.width // 2 - 12, enemy.y + enemy.height // 2, "sub_shot_up")
                            self.items.append(item_to_drop)
                        elif rand_val < 0.10 + 0.05 + 0.10: 
                            item_to_drop = Item(enemy.x + enemy.width // 2 - 12, enemy.y + enemy.height // 2, "shot_up")
                            self.items.append(item_to_drop)
                        
                        hit_enemy = True 
                        break 
                if bullet.active: 
                    new_player_bullets.append(bullet)
        self.player_bullets = new_player_bullets 
        # **[変更終了]**


        # **[変更開始] 敵の弾の更新と衝突判定を最適化**
        new_enemy_bullets = [] 
        for bullet in self.enemy_bullets:
            bullet.update()
            if not bullet.active: 
                continue 
            
            if self.player.hit_timer <= 0 and bullet.check_collision(self.player): 
                self.player.life -= 1 
                print(f"弾がプレイヤーに命中！残りライフ：{self.player.life}")
                self.player.hit_timer = self.player.invincible_duration 
                
                if self.player.life <= 0:
                    if game_over_hit_sound:
                        game_over_hit_sound.play()
                else:
                    if player_hit_sound:
                        player_hit_sound.play()

                if self.player.life <= 0:
                    if not self.game_over:
                        self.player.alive = False
                        self.game_over = True
                        print("ゲームオーバー")
                if self.game_over:
                    break 
            else: 
                if bullet.speed_y == -7: # サブ機体の弾は上向き
                    for enemy in self.enemies:
                        if bullet.check_collision(enemy): 
                            self.score += 100 
                            break 
                    else: 
                        if bullet.active: 
                            new_enemy_bullets.append(bullet)
                else: 
                    if bullet.active: 
                        new_enemy_bullets.append(bullet)
        self.enemy_bullets = new_enemy_bullets 
        # **[変更終了]**

        for item in self.items[:]:
            item.update()
            if not item.active:
                self.items.remove(item)
            elif item.check_collision(self.player):
                if item.item_type == "shot_up": 
                    self.player.shot_count += 1
                    print(f"ショット数アップ！現在のショット数: {self.player.shot_count}")
                elif item.item_type == "sub_shot_up": 
                    if len(self.sub_players) == 0:
                        self.sub_players.append(SubPlayer(self.player, -1)) 
                        print("左サブ機体を追加！")
                    elif len(self.sub_players) == 1:
                        self.sub_players.append(SubPlayer(self.player, 1)) 
                        print("右サブ機体を追加！")
                    else:
                        print("サブ機体はこれ以上追加できません。") 
                elif item.item_type == "score_x2":
                    self.score_multiplier = 2
                    self.score_multiplier_timer = 10 * 60 
                    print("スコア2倍！10秒間有効！")
                self.items.remove(item)

        for sub_player in self.sub_players:
            if sub_player.alive:
                new_bullets = sub_player.update()
                self.enemy_bullets.extend(new_bullets) 

        self.spawn_timer += 1
        if self.spawn_timer >= self.current_spawn_interval:
            type_id = random.choice([0, 1, 2])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -30, type_id)
            self.enemies.append(enemy)
            self.spawn_timer = 0

        for enemy in self.enemies:
            if enemy.alive:
                enemy.update() 
                # 敵とプレイヤーの接触判定
                if self.player.hit_timer <= 0 and \
                   (enemy.x < self.player.x + self.player.width and
                    enemy.x + enemy.width > self.player.x and
                    enemy.y < self.player.y + self.player.height and
                    enemy.y + enemy.height > self.player.y):
                    
                    self.player.life -= 1 
                    print(f"敵がプレイヤーに接触！残りライフ：{self.player.life}")
                    enemy.alive = False
                    self.player.hit_timer = self.player.invincible_duration # 無敵時間開始

                    # ヒット音の再生
                    if self.player.life <= 0:
                        if game_over_hit_sound:
                            game_over_hit_sound.play()
                    else:
                        if player_hit_sound:
                            player_hit_sound.play()

                    if self.player.life <= 0:
                        if not self.game_over:
                            self.player.alive = False
                            self.game_over = True
                            print("ゲームオーバー")
                    if self.game_over:
                        break 

                if enemy.should_shoot():
                    bullet = Bullet(enemy.x + enemy.width // 2, enemy.y + enemy.height, 4, YELLOW, 0) 
                    self.enemy_bullets.append(bullet)
                    enemy.reset_shoot_timer()

        if self.score >= self.spawn_interval_decrease_threshold and self.current_spawn_interval > 10:
            self.current_spawn_interval = max(10, self.current_spawn_interval - self.spawn_decrease_amount)
            self.spawn_interval_decrease_threshold += 500

        while self.score >= self.next_enemy_add_score:
            type_id = random.choice([0, 1, 2])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -random.randint(50, 200), type_id) 
            self.enemies.append(enemy)
            self.next_enemy_add_score += 200 
            print(f"スコア {self.score} で新しい敵を追加。現在の敵数: {len(self.enemies)}")

        while self.score >= self.next_speed_increase_score:
            for enemy in self.enemies:
                enemy.speed_y *= 1.15 
                enemy.speed_x *= 1.15
            self.next_speed_increase_score += 500 
            print(f"スコア {self.score} で敵の速度が上昇。")

        self.enemies = [enemy for enemy in self.enemies if enemy.alive and enemy.y < SCREEN_HEIGHT]

        if not self.player.alive: 
            self.game_over = True

    def draw(self):
        screen.fill(BLACK)

        self.player.draw(screen)

        self.player.draw_life(screen)

        for enemy in self.enemies:
            enemy.draw(screen)
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.draw(screen)
        for item in self.items: 
            item.draw(screen)
        for sub_player in self.sub_players:
            sub_player.draw(screen)

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
            
            if not self.game_over: 
                self.update()
                self.draw()
            else: 
                self.draw() 
                self.save_score_to_server()
                pygame.time.wait(3000) 
                running = False 

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def save_score_to_server(self):
        """スコアをサーバーに送信"""
        try:
            print(f"\nゲームオーバー! 最終スコア: {self.score}")

            # サーバーにスコアを送信
            data = {"player_name": self.player_name, "score": self.score}

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


# ゲームの実行
if __name__ == "__main__":
    Game().run()