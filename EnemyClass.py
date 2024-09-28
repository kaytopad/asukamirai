import pygame as pg
import random

class Enemy:
    def __init__(self, img_path):
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rects = []  # 敵の矩形を格納するリスト

    def spawn_enemy(self):
        # 敵の新しい矩形を生成し、リストに追加
        new_rect = self.image.get_rect()
        new_rect.x = random.randint(0, 800 - new_rect.width)  # ランダムに初期位置を設定
        new_rect.y = 0  # 上から出現
        self.rects.append(new_rect)  # 生成した敵をリストに追加

    def update(self):
        for rect in self.rects:
            rect.y += 5  # 下に移動

            # 敵を左右にブーメランのように動かす
            rect.x += 5 * (-1 if (rect.y // 20) % 2 == 0 else 1)  # 簡単な左右移動

            # 画面の端で反転
            if rect.x < 0:
                rect.x = 0
            elif rect.x > 800 - rect.width:
                rect.x = 800 - rect.width

            # 敵が画面外に出たら削除（必要に応じて）
            if rect.y > 600:  # 画面下に出たら
                self.rects.remove(rect)  # 敵を削除

    def draw(self, screen):
        for rect in self.rects:
            screen.blit(self.image, rect)

    def check_collision(self, bullet_rect, player_rect):
        for rect in self.rects:
            if rect.colliderect(bullet_rect) or rect.colliderect(player_rect):
                return True
        return False


