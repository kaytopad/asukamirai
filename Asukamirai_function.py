import pygame as ps,sys
import random

#弾の処理

def bullet(bulletrect,myrect):
    bulletrect.x = myrect.x + 25 - 8
    bulletrect.y = myrect.y

def bulletAftter(bulletimg,bulletrect,myrect,screen):
    bulletrect.y += -15
    screen.blit(bulletimg,bulletrect)

#UFOの処理

def ufodisplay(ufo,myrect,bulletrect,score,page):
    if ufo.y > 600:
        ufo.x = random.randint(0,800)
        ufo.y = -100
#自機とUFOの衝突
    if ufo.colliderect(myrect):
        page = 2
    if ufo.colliderect(bulletrect):
        score = score + 1000
        ufo.y = -100
        ufo.x = random.randint(0,800)
        bulletrect.y = -100
    return score
