import pygame as pg

class Bullet:
    def __init__(self,img_path):
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image,(50,50))
        self.rect = pg.Rect(400,-100,50,50)
    
    def shoot(self,player_rect):
        self.rect.x = player_rect.x + 25 -8
        self.rect.y = player_rect.y
    
    def update(self):
        if self.rect.y >= 0:
            self.rect.y += -15
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)

    