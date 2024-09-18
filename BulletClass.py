import pygame as pg

class Bullet:
    def __init__(self, img_path):
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = pg.Rect(-100, -100, 10, 30)  # 初期位置は画面外
        self.speed = -10

    def shoot(self, player_rect):
        # プレイヤーの位置から発射
        self.rect.x = player_rect.x + player_rect.width // 2 - self.rect.width // 2
        self.rect.y = player_rect.y

    def update(self):
        # 弾を上方向に移動
        self.rect.y += self.speed

        # 弾が画面外に出たらリセット
        if self.rect.y < 0:
            self.rect.y = -100  # 画面外に移動させて、次の発射を待つ

    def draw(self, screen):
        # 弾を描画
        screen.blit(self.image, self.rect)


    