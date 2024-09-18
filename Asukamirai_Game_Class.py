import pygame as pg
import sys
import random
from PlayerClass import Player
from EnemyClass import Enemy
from ButtonClass import Button
from BulletClass import Bullet

class Game:
    def __init__(self,screen):
        self.screen = screen
        self.page = 1
        self.push_flag = False
        self.score = 0
        self.player = Player("./image/Renjer(Blue).png",800)
        self.bullet = Bullet("./image/mybullet.tga")
        self.enemy = Enemy("./image/enemy1.tga")
        self.replay_button = Button("./image/btn006_08.gif",(360,400))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
    
    def game_stage(self):
        self.screen.fill(pg.Color("BLACK"))
        mx,my = pg.mouse.get_pos()
        mdown = pg.mouse.get_pressed()

        self.player.update(mx)

        if mdown[0] and self.bullet.rect.y < 0:
            self.bullet.shoot(self.player.rect)
        self.bullet.update()

        #Player＆Bullet描画
        self.player.draw(self.screen)
        self.bullet.draw(self.screen)
        #Enemy更新＆描画
        if self.enemy.update(self.player.rect):
            self.page = 2  # 衝突したらゲームオーバー
        self.enemy.draw(self.screen)

        #当たり判定
        for enemy_rect in self.enemy.rects:
            if self.bullet.rect.colliderect(enemy_rect):
                self.score += 100
                self.enemy.rects.remove(enemy_rect)  # 当たった敵を削除
                self.bullet.rect.y = -100
        #衝突判定
        if self.enemy.check_collision(self.bullet.rect,self.player.rect):
            #GameOverFlag
            self.page = 2
        
        #Score描画
        font = pg.font.Font(None,40)
        score_text = font.render(f"SCORE: {self.score}", True, pg.Color("WHITE"))
        self.screen.blit(score_text,(20,20))

    #GameOverメソッド
    def game_ovre(self):
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

    #ReStartメソッド
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
                self.game_ovre()

