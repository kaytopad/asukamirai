import pygame as pg
import random

class Enemy:
    def __init__(self,image_path):
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image,(50,50))
        self.rects = [pg.rect(random.randint(0,800),-100 * i,50,50)for i in range(10)]
        
def update(self):
    for rect in self.rects:
        rect.y += 10

def draw(self,screen):
    for rect in self.rects:
        screen.blit(self.image,rect)

def check_collision(self,bullet_rect,player_rect):
    for rect in self.rects:
        if rect.colliderect(player_rect):
            return True
        if rect.colliderect(bullet_rect):
            rect.x = random.randint(0,800)
            rect.y = -100
            return True
    return False