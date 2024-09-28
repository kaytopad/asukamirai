import pygame as pg
import sys
import random
from PlayerClass import Player
from EnemyClass import Enemy
from ButtonClass import Button
from BulletClass import Bullet

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.page = 1
        self.push_flag = False
        self.score = 0
        self.player = Player("./image/Renjer(Blue).png", 800)
        self.bullet = Bullet("./image/mybullet.tga")
        self.enemy = Enemy("./image/enemy1.tga")
        self.replay_button = Button("./image/btn006_08.gif", (360, 400))
        self.bullets = []
        self.enemy_spawn_timer = 0  # 敵を生成するタイマー
        self.enemy_spawn_interval = 2000  # 敵の生成間隔（2000ミリ秒 = 2秒）
        self.max_enemies = 5  # 最大の敵の数
        self.last_shot_time = 0  # 最後に弾を発射した時間
        self.shot_interval = 500  # 弾を発射する間隔（500ミリ秒 = 0.5秒）

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def game_stage(self):
        self.screen.fill(pg.Color("BLACK"))
        keys = pg.key.get_pressed()

        # プレイヤーの移動
        if keys[pg.K_a]:
            self.player.rect.x -= 5
        if keys[pg.K_d]:
            self.player.rect.x += 5

        # 弾の発射（連射可能）
        current_time = pg.time.get_ticks()
        if keys[pg.K_p] and current_time - self.last_shot_time > self.shot_interval:
            self.bullet.shoot(self.player.rect)
            self.last_shot_time = current_time  # 最後の発射時間を更新

        self.bullet.update()

        # プレイヤーと弾を描画
        self.player.draw(self.screen)
        self.bullet.draw(self.screen)

        # 敵の生成タイミングと最大数の制限
        self.enemy_spawn_timer += pg.time.get_ticks()
        if self.enemy_spawn_timer > self.enemy_spawn_interval and len(self.enemy.rects) < self.max_enemies:
            self.enemy.spawn_enemy()  # 敵を生成
            self.enemy_spawn_timer = 0  # タイマーをリセット

        # 敵の更新と描画
        self.enemy.update()
        self.enemy.draw(self.screen)

        # 当たり判定
        for enemy_rect in self.enemy.rects:
            if self.bullet.rect.colliderect(enemy_rect):
                self.score += 100
                self.enemy.rects.remove(enemy_rect)  # 当たった敵を削除
                self.bullet.rect.y = -100

        # 衝突判定
        if self.enemy.check_collision(self.bullet.rect, self.player.rect):
            self.page = 2  # ゲームオーバー

        # スコアを描画
        font = pg.font.Font(None, 40)
        score_text = font.render(f"SCORE: {self.score}", True, pg.Color("WHITE"))
        self.screen.blit(score_text, (20, 20))

    # ゲームオーバー画面
    def game_over(self):
        self.screen.fill(pg.Color("NAVY"))
        font = pg.font.Font(None, 150)
        text = font.render("GAMEOVER", True, pg.Color("RED"))
        self.screen.blit(text, (100, 200))

        self.replay_button.draw(self.screen)

        font = pg.font.Font(None, 40)
        score_text = font.render(f"SCORE: {self.score}", True, pg.Color("WHITE"))
        self.screen.blit(score_text, (20, 20))

        mx, my = pg.mouse.get_pos()
        mdown = pg.mouse.get_pressed()
        if self.replay_button.is_clicked(mx, my, mdown):
            self.page = 1
            self.reset_game()

    # ゲームをリセット
    def reset_game(self):
        self.score = 0
        self.bullet.rect.y = -100
        self.enemy = Enemy("./image/enemy1.tga")

    def run(self):
        while True:
            pg.display.update()
            pg.time.Clock().tick(60)

            self.handle_events()

            if self.page == 1:
                self.game_stage()
            elif self.page == 2:
                self.game_over()
