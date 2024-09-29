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
        self.bullet_image_path = "./image/mybullet.tga"
        self.bullets = []  # 弾を格納するリスト
        self.enemy = Enemy("./image/enemy1.tga")
        self.replay_button = Button("./image/btn006_08.gif", (360, 400))
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 2000
        self.max_enemies = 5
        self.last_shot_time = 0
        self.shot_interval = 500

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
        if keys[pg.K_w]:
            self.player.rect.y -= 5
        if keys[pg.K_s]:
            self.player.rect.y += 5

        # 弾の発射
        current_time = pg.time.get_ticks()
        if keys[pg.K_p] and current_time - self.last_shot_time > self.shot_interval:
            bullet = Bullet(self.bullet_image_path)  # 新しい弾を生成
            bullet.shoot(self.player.rect)
            self.bullets.append(bullet)  # リストに追加
            self.last_shot_time = current_time

        # 弾の更新と描画
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.y < 0:  # 弾が画面外に出たらリストから削除
                self.bullets.remove(bullet)

        # プレイヤーと弾を描画
        self.player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # 敵の生成タイミングと最大数の制限
        self.enemy_spawn_timer += pg.time.get_ticks()
        if self.enemy_spawn_timer > self.enemy_spawn_interval and len(self.enemy.rects) < self.max_enemies:
            self.enemy.spawn_enemy()
            self.enemy_spawn_timer = 0

        # 敵の更新と描画
        self.enemy.update()
        self.enemy.draw(self.screen)

        # 当たり判定
        collision, enemy_rect = self.enemy.check_collision([bullet.rect for bullet in self.bullets], self.player.rect)
        if collision:
            if enemy_rect:
                self.enemy.rects.remove(enemy_rect)  # 当たった敵を削除
                self.score += 100
            else:
                self.page = 2  # プレイヤーに衝突でゲームオーバー

        # スコアを描画
        font = pg.font.Font(None, 40)
        score_text = font.render(f"SCORE: {self.score}", True, pg.Color("WHITE"))
        self.screen.blit(score_text, (20, 20))

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

    def reset_game(self):
        self.score = 0
        self.bullets.clear()  # 弾リストをクリア
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
