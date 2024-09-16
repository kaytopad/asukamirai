import pygame as pg,sys

class Player:
    def __init__(self,img_path,sceen_width):
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image,(50,50))
        self.rect = pg.Rect(sceen_width//2,500,50,50)
    
    def update(self,mx):
        self.rect.x = mx -25
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)
