import pygame as pg
import sys
from PlayerClass import Player
from EnemyClass import Enemy
from ButtonClass import Button
from BulletClass import Bullet

class Game:
    def __init__(self):
        self.page = 1
        self.push_flag = False
        self.score = 0
        self.player = Player("./image/Renjer(Blue)",800)
        self.bullet = Bullet("./image/mybullet.tga")
        self.enemy = Enemy("./image/enemy.tga")
        self.replay_button = Button("./image/btn006_08.gif",(360,400))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
    
    def game_stage(self):
        
        
