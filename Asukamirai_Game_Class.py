import pygame as pg
import sys
from PlayerClass import Player
from EnemyClass import Enemy
from ButtonClass import Button
from BulletClass import Bullet

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.page = 1
        self.score = 0
        self.player = Player("./image/Renjer(Blue).png", 800)
        self.enemy = Enemy("./image/enemy1.tga")
        self.replay_button = Button("./image/btn006_08.gif", (360, 400))
        self.bullets = []  # 弾を格納するリスト
        self.bullet_img_path = "./image/mybullet.tga"  # 弾の画像パス
        self.last_shot_time = 0  # 最後に弾を撃った時間
        self.shoot_interval = 300  # 連射の間隔（ミリ秒）

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def game_stage(self):
        self.screen.fill(pg.Color("BLACK"))
        keys = pg.key.get_pressed()  # 現在のキーボード入力を取得

        # プレイヤーの更新と描画
        if keys[pg.K_a]:  # Aキーで左に移動
            self.player.rect.x -= 5
        if keys[pg.K_d]:  # Dキーで右に移動
            self.player.rect.x += 5

        self.player.draw(self.screen)

        # 弾を発射するタイミングの管理（連射の間隔チェック）
        current_time = pg.time.get_ticks()
        if keys[pg.K_p] and current_time - self.last_shot_time > self.shoot_interval:
            bullet = Bullet(self.bullet_img_path)
            bullet.shoot(self.player.rect)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

        # 発射された弾の更新と描画
        for bullet in self.bullets[:]:  # bulletsのコピーを使ってループ
            bullet.update()
            bullet.draw(self.screen)
            # 弾が画面外に出たら削除
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)

        # 敵の更新と描画
        if self.enemy.update(self.player.rect):
            self.page = 2  # 衝突したらゲームオーバー
        self.enemy.draw(self.screen)

        # 弾と敵の衝突判定
        for bullet in self.bullets[:]:  # bulletsのコピーを使ってループ
            for enemy_rect in self.enemy.rects[:]:  # enemy.rectsのコピー
                if bullet.rect.colliderect(enemy_rect):
                    self.score += 100
                    self.enemy.rects.remove(enemy_rect)  # 当たった敵を削除
                    self.bullets.remove(bullet)  # 当たった弾を削除
                    break  # 一度に複数の敵に当たらないようにループを終了
        
        # 弾とプレイヤーの衝突判定（ゲームオーバー）
        for bullet in self.bullets:
            if self.enemy.check_collision(bullet.rect, self.player.rect):
                self.page = 2  # ゲームオーバー

        # スコアの描画
        font = pg.font.Font(None, 40)
        score_text = font.render(f"SCORE: {self.score}", True, pg.Color("WHITE"))
        self.screen.blit(score_text, (20, 20))

    # ゲームオーバー画面の処理
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

    # ゲームのリセット処理
    def reset_game(self):
        self.score = 0
        self.bullets = []  # 弾のリストをリセット
        self.enemy = Enemy("./image/enemy1.tga")  # 敵を再生成

    # メインループ
    def run(self):
        while True:
            pg.display.update()
            pg.time.Clock().tick(60)
            
            self.handle_events()

            if self.page == 1:
                self.game_stage()
            elif self.page == 2:
                self.game_over()
