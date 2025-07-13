import random

from game.actors.bullet import Bullet
from game.actors.enemy import Enemy
from game.actors.item import Item
from game.actors.player import Player
from game.actors.subPlayer import SubPlayer
from game.utils.config import SCREEN_HEIGHT, SCREEN_WIDTH, YELLOW


class GameCore:
    """ゲームのコアロジックを管理するクラス"""

    def __init__(self, images, sounds, player_name="Player1"):
        """初期化関数"""
        self.images = images
        self.sounds = sounds
        self.player_name = player_name
        self.player = Player(self.images)
        self.reset_game()

    def reset_game(self):
        """ゲームの状態をリセットする関数"""
        self.player = Player(self.images)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.items = []
        self.sub_players = []
        self.sub_shot_up_timers = []
        self.score = 0
        self.spawn_timer = 0
        self.shot_up_timer = 0
        self.sub_shot_up_timer = 0
        self.game_over = False

        # 敵の追加・スピードアップ関連
        self.next_enemy_add_score = 200
        self.next_speed_increase_score = 1000

        # 敵の生成間隔関連
        self.initial_spawn_interval = 60
        self.current_spawn_interval = self.initial_spawn_interval
        self.spawn_interval_decrease_threshold = 500
        self.spawn_decrease_amount = 5

        # スコア倍率関連
        self.score_multiplier = 1
        self.score_multiplier_timer = 0

        # 初期敵の配置
        self._spawn_initial_enemies()

    def _spawn_initial_enemies(self):
        """初期の敵を生成する関数"""
        for _ in range(3):
            type_id = random.choice([0, 1])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -random.randint(50, 300), type_id, self.images)
            self.enemies.append(enemy)

    def update(self):
        """ゲームの状態を更新する関数"""
        if self.game_over:
            return

        self.player.update()  # プレイヤーの更新
        self._update_player_bullets()  # プレイヤーの弾の更新
        self._update_enemy_bullets()  # 敵の弾の更新
        self._update_items()  # アイテムの更新
        self._update_sub_players()  # サブプレイヤーの更新
        self._spawn_enemies()  # 敵の生成
        self._update_enemies()  # 敵の更新
        self._adjust_spawn_interval()  # 敵生成間隔の調整
        self._add_enemies_by_score()  # スコアに応じた敵の追加
        self._increase_enemy_speed_by_score()  # スコアに応じた敵の速度上昇
        self._remove_offscreen_enemies()  # 画面外の敵を削除
        self._update_effect_timers()  # 効果のタイマー更新
        self._update_score_multiplier_timer()  # スコア倍率タイマーの更新

        # プレイヤーの生存確認
        if not self.player.alive:
            self.game_over = True

    def _update_player_bullets(self):
        """プレイヤーの弾を更新する関数"""
        new_player_bullets = []
        for bullet in self.player_bullets:
            bullet.update()
            if not bullet.active:
                continue

            # 敵との衝突判定
            hit_enemy = False
            for enemy in self.enemies:
                if bullet.check_collision(enemy):
                    self.score += 100 * self.score_multiplier
                    self._drop_item(enemy)
                    hit_enemy = True
                    break

            # 弾がまだ有効な場合のみリストに追加
            if not hit_enemy:
                new_player_bullets.append(bullet)

        self.player_bullets = new_player_bullets

    def _drop_item(self, enemy):
        """敵を倒したときにアイテムをドロップする関数"""
        # アイテムドロップ確率の定数
        SCORE_X2_PROBABILITY = 0.10
        SUB_SHOT_UP_PROBABILITY = 0.15
        SHOT_UP_PROBABILITY = 0.25

        rand_val = random.random()
        item_x = enemy.x + enemy.width // 2 - 12
        item_y = enemy.y + enemy.height // 2

        if rand_val < SCORE_X2_PROBABILITY:
            item = Item(item_x, item_y, "score_x2", self.images)
            self.items.append(item)
        elif rand_val < SUB_SHOT_UP_PROBABILITY:
            item = Item(item_x, item_y, "sub_shot_up", self.images)
            self.items.append(item)
        elif rand_val < SHOT_UP_PROBABILITY:
            item = Item(item_x, item_y, "shot_up", self.images)
            self.items.append(item)

    def _update_enemy_bullets(self):
        """敵の弾を更新する関数"""
        new_enemy_bullets = []
        for bullet in self.enemy_bullets:
            bullet.update()
            if not bullet.active:
                continue

            # プレイヤーとの衝突判定
            if self.player.hit_timer <= 0 and bullet.check_collision(self.player):
                self._player_hit()
                if self.game_over:
                    break
                continue

            # 特殊な弾（上向きの弾）の処理
            if bullet.speed_y == -7:
                hit_enemy = False
                for enemy in self.enemies:
                    if bullet.check_collision(enemy):
                        self.score += 100 * self.score_multiplier
                        hit_enemy = True
                        break

                if not hit_enemy:
                    new_enemy_bullets.append(bullet)
            else:
                new_enemy_bullets.append(bullet)

        self.enemy_bullets = new_enemy_bullets

    def _player_hit(self):
        """プレイヤーが敵の弾に当たったときの処理"""
        self.player.life -= 1
        print(f"弾がプレイヤーに命中！残りライフ：{self.player.life}")
        self.player.hit_timer = self.player.invincible_duration

        # ライフが0になったかの判定
        if self.player.life <= 0:
            self._handle_game_over()
        else:
            self._play_sound("player_hit")

    def _handle_game_over(self):
        """ゲームオーバー処理"""
        if not self.game_over:
            self.player.alive = False
            self.game_over = True
            print("ゲームオーバー")
            self._play_sound("game_over_hit")

    def _play_sound(self, sound_name):
        """サウンドを再生する関数"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

    def _update_items(self):
        """アイテムを更新する関数"""
        for item in self.items[:]:  # スライスでコピーを作成
            item.update()
            if not item.active:
                self.items.remove(item)
            elif item.check_collision(self.player):
                self._apply_item_effect(item)
                self.items.remove(item)

    def _apply_item_effect(self, item):
        """アイテムの効果を適用する関数"""
        # 効果時間の定数
        SHOT_UP_DURATION = 10 * 60  # 10秒間
        SCORE_X2_DURATION = 3 * 60  # 3秒間

        if item.item_type == "shot_up":
            self.player.shot_count += 1
            self.shot_up_timer = SHOT_UP_DURATION
            print(f"ショット数アップ！現在のショット数: {self.player.shot_count}")

        elif item.item_type == "sub_shot_up":
            self._add_sub_player()

        elif item.item_type == "score_x2":
            self.score_multiplier = 2
            self.score_multiplier_timer = SCORE_X2_DURATION
            print("スコア2倍！3秒間有効！")

    def _add_sub_player(self):
        """サブプレイヤーを追加する関数"""
        MAX_SUB_PLAYERS = 2
        SUB_SHOT_UP_DURATION = 10 * 60

        if len(self.sub_players) < MAX_SUB_PLAYERS:
            # 左側から追加
            side = -1 if len(self.sub_players) == 0 else 1
            sub_player = SubPlayer(self.player, side)
            self.sub_players.append(sub_player)
            self.sub_shot_up_timers.append(SUB_SHOT_UP_DURATION)

            side_name = "左" if side == -1 else "右"
            print(f"{side_name}サブ機体を追加！")
        else:
            print("サブ機体はこれ以上追加できません。")

    def _update_effect_timers(self):
        """効果のタイマーを更新する関数"""
        # ショット数アップ効果のタイマー
        if self.shot_up_timer > 0:
            self.shot_up_timer -= 1
            if self.shot_up_timer == 0:
                self.player.shot_count = max(1, self.player.shot_count - 1)
                print("ショット数アップ効果が終了しました。")

        # サブ機体追加効果のタイマー
        for i in reversed(range(len(self.sub_shot_up_timers))):
            self.sub_shot_up_timers[i] -= 1
            if self.sub_shot_up_timers[i] <= 0:
                if i < len(self.sub_players):
                    self.sub_players.pop(i)
                self.sub_shot_up_timers.pop(i)
                print("サブ機体が消失しました。")

    def _update_sub_players(self):
        """サブプレイヤーを更新する関数"""
        for sub_player in self.sub_players:
            if sub_player.alive:
                new_bullets = sub_player.update()
                if new_bullets:  # None チェック
                    self.enemy_bullets.extend(new_bullets)

    def _spawn_enemies(self):
        """敵を生成する関数"""
        self.spawn_timer += 1
        if self.spawn_timer >= self.current_spawn_interval:
            self._create_enemy()
            self.spawn_timer = 0

    def _create_enemy(self):
        """敵を作成する関数"""
        type_id = random.choice([0, 1, 2])
        x = random.randint(0, SCREEN_WIDTH - 40)
        enemy = Enemy(x, -30, type_id, self.images)
        self.enemies.append(enemy)

    def _update_enemies(self):
        """敵を更新する関数"""
        for enemy in self.enemies:
            if not enemy.alive:
                continue

            enemy.update()

            # プレイヤーとの衝突判定
            if self._check_enemy_player_collision(enemy):
                self._enemy_hit_player(enemy)
                if self.game_over:
                    break

            # 敵の射撃処理
            if enemy.should_shoot():
                self._enemy_shoot(enemy)

    def _check_enemy_player_collision(self, enemy):
        """敵とプレイヤーの衝突判定"""
        if self.player.hit_timer > 0:
            return False

        return (
            enemy.x < self.player.x + self.player.width
            and enemy.x + enemy.width > self.player.x
            and enemy.y < self.player.y + self.player.height
            and enemy.y + enemy.height > self.player.y
        )

    def _enemy_shoot(self, enemy):
        """敵の射撃処理"""
        bullet = Bullet(
            enemy.x + enemy.width // 2, enemy.y + enemy.height, 4, YELLOW, 0
        )
        self.enemy_bullets.append(bullet)
        enemy.reset_shoot_timer()

    def _enemy_hit_player(self, enemy):
        """敵がプレイヤーに接触したときの処理"""
        self.player.life -= 1
        print(f"敵がプレイヤーに接触！残りライフ：{self.player.life}")
        enemy.alive = False
        self.player.hit_timer = self.player.invincible_duration

        if self.player.life <= 0:
            self._handle_game_over()
        else:
            self._play_sound("player_hit")

    def _adjust_spawn_interval(self):
        """敵生成間隔を調整する関数"""
        MIN_SPAWN_INTERVAL = 10

        if (
            self.score >= self.spawn_interval_decrease_threshold
            and self.current_spawn_interval > MIN_SPAWN_INTERVAL
        ):
            self.current_spawn_interval = max(
                MIN_SPAWN_INTERVAL,
                self.current_spawn_interval - self.spawn_decrease_amount,
            )
            self.spawn_interval_decrease_threshold += 500

    def _add_enemies_by_score(self):
        """スコアに応じて敵を追加する関数"""
        ENEMY_ADD_INTERVAL = 300

        while self.score >= self.next_enemy_add_score:
            type_id = random.choice([0, 1, 2])
            x = random.randint(0, SCREEN_WIDTH - 40)
            enemy = Enemy(x, -random.randint(50, 200), type_id, self.images)
            self.enemies.append(enemy)
            self.next_enemy_add_score += ENEMY_ADD_INTERVAL
            print(
                f"スコア {self.score} で新しい敵を追加。現在の敵数: {len(self.enemies)}"
            )

    def _increase_enemy_speed_by_score(self):
        """スコアに応じて敵の速度を上昇させる関数"""
        SPEED_INCREASE_INTERVAL = 1000
        SPEED_MULTIPLIER = 1.02

        while self.score >= self.next_speed_increase_score:
            for enemy in self.enemies:
                enemy.speed_y *= SPEED_MULTIPLIER
                enemy.speed_x *= SPEED_MULTIPLIER
            self.next_speed_increase_score += SPEED_INCREASE_INTERVAL
            print(f"スコア {self.score} で敵の速度が上昇。")

    def _remove_offscreen_enemies(self):
        """画面外の敵を削除する関数"""
        self.enemies = [
            enemy for enemy in self.enemies if enemy.alive and enemy.y < SCREEN_HEIGHT
        ]

    def _update_score_multiplier_timer(self):
        """スコア倍率タイマーを更新する関数"""
        if self.score_multiplier_timer > 0:
            self.score_multiplier_timer -= 1
            if self.score_multiplier_timer == 0:
                self.score_multiplier = 1
                print("スコア2倍効果が終了しました。")
