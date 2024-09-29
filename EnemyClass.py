import pygame as pg
import random

class Enemy:
    def __init__(self, img_path):
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rects = []  # 敵の矩形を格納するリスト

    def spawn_enemy(self):
        new_rect = self.image.get_rect()
        new_rect.x = random.randint(0, 800 - new_rect.width)
        new_rect.y = 0
        self.rects.append(new_rect)

    def update(self):
        for rect in self.rects:
            rect.y += 5  # 下に移動
            rect.x += 5 * (-1 if (rect.y // 20) % 2 == 0 else 1)  # ブーメランのように左右移動

            if rect.x < 0:
                rect.x = 0
            elif rect.x > 800 - rect.width:
                rect.x = 800 - rect.width

            if rect.y > 600:  # 画面下に出たら削除
                self.rects.remove(rect)

    def draw(self, screen):
        for rect in self.rects:
            screen.blit(self.image, rect)

    def check_collision(self, bullet_rects, player_rect):
        #""" 弾またはプレイヤーとの衝突を確認するメソッド """
        for rect in self.rects:
            # 弾との衝突をチェック
            for bullet_rect in bullet_rects:
                if rect.colliderect(bullet_rect):
                    return True, rect  # 弾に衝突した敵の矩形を返す
            
            # プレイヤーとの衝突をチェック
            if rect.colliderect(player_rect):
                return True, None  # プレイヤーに衝突した場合、Noneを返す

        return False, None  # 衝突がない場合
