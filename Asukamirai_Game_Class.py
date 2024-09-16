import pygame as ps
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
        
