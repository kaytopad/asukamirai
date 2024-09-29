import pygame as pg
from Asukamirai_Game_Class import Game

pg.init()
screen = pg.display.set_mode((800, 600))

if __name__ == "__main__":
    game = Game(screen)
    game.run()
    