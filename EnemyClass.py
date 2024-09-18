import pygame as pg
import random

class Enemy:
    def __init__(self, image_path):
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rects = []  # 敵を管理するリスト
        self.speeds = []  # 各敵のx方向の速度を管理するリスト
        self.spawn_delay = 15  # 敵を出現させるフレーム数の間隔
        self.frame_count = 0  # フレームカウントの初期値
        self.speed = 5  # 左右に動くスピード

    def update(self, player_rect):
        self.frame_count += 1
        # 一定のフレーム数ごとに敵を生成
        if self.frame_count % self.spawn_delay == 0:
            new_enemy = pg.Rect(random.randint(0, 750), -50, 50, 50)
            new_speed = self.speed  # 新しい敵の初期速度
            self.rects.append(new_enemy)
            self.speeds.append(new_speed)

        # 既存の敵の移動（左右と縦方向）
        for i in range(len(self.rects) - 1, -1, -1):  # リストを逆順にループ
            rect = self.rects[i]
            rect.x += self.speeds[i]  # 敵のx座標に速度を適用
            rect.y += 5  # 下方向への移動

            # 画面端に来たら方向を反転
            if rect.x <= 0 or rect.x >= 750:
                self.speeds[i] *= -1  # x方向の移動を反転

            # プレイヤーとの衝突
            if rect.colliderect(player_rect):
                return True  # 衝突したらTrueを返す

            # 画面外に出たら削除
            if rect.y > 600:
                del self.rects[i]
                del self.speeds[i]

        return False  # プレイヤーと衝突しなければFalseを返す

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
                del self.speeds[i]
                return True  # 衝突があればTrueを返す

        return False  # 衝突がなければFalseを返す