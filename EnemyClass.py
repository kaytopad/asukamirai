import pygame as pg
import random

class Enemy:
    def __init__(self, image_path):
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rects = []  # 敵を管理するリスト
        self.speeds_y = []  # 敵のY方向の速度を管理するリスト
        self.spawn_delay = 10  # 敵を出現させるフレーム数の間隔
        self.frame_count = 0  # フレームカウントの初期値
        self.speed_y = 5  # 敵が下に動くスピード

    def update(self, player_rect):
        self.frame_count += 1
        # 一定のフレーム数ごとに敵を生成
        if self.frame_count % self.spawn_delay == 0:
            new_enemy = pg.Rect(random.randint(0, 750), -50, 50, 50)  # 横方向にランダムに生成
            self.rects.append(new_enemy)
            self.speeds_y.append(self.speed_y)

        # 既存の敵を下方向に移動させる
        for i, rect in enumerate(self.rects):
            rect.y += self.speeds_y[i]  # Y方向に移動

            # 画面外に出たら削除
            if rect.y > 600:  # 画面下に出たら削除
                del self.rects[i]
                del self.speeds_y[i]

            # プレイヤーと衝突した場合の処理
            if rect.colliderect(player_rect):
                return True  # 衝突したらTrueを返す

        return False  # 衝突がなければFalseを返す

    def draw(self, screen):
        for rect in self.rects:
            screen.blit(self.image, rect)

    def check_collision(self, bullet_rect, player_rect):
        for i in range(len(self.rects) - 1, -1, -1):  # リストを逆順にループ
            rect = self.rects[i]
            # プレイヤーと敵の衝突
            if rect.colliderect(player_rect):
                return True
            # 弾丸と敵の衝突
            if rect.colliderect(bullet_rect):
                # 敵が弾丸に当たったら削除
                del self.rects[i]
                del self.speeds_y[i]
                return True  # 衝突があればTrueを返す

        return False  # 衝突がなければFalseを返す
