import pygame as pg

class Button:
    def __init__(self,img_path,position):
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect(topleft = position)
    def draw(self,screen):
        screen.blit(self.image,self.rect)
    def is_clicked(self,mx,my,mdown):
        if mdown[0] and self.rect.collidepoint(mx,my):
            return True
        return False