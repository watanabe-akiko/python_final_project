import pygame as pg

# from bullet import Bullet # 弾クラスをインポート
# 1200 676
# ボタン押しながら
class Fish:
    def __init__(self, x, y, screen, key):
        self.img = pg.image.load("images/fish_sakana_sake.png")
        self.size = 100
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        self.player_pos = self.img.get_rect()  # 画像の矩形情報(player_rect)を取得
        self.player_pos.x = x
        self.player_pos.y = y
        # 右を向いているかどうかのフラグ #右向き：True 左向き：False
        self.fRight = True
        # 移動量
        self.move_amount = 10

        # 体力
        self.player_hp = 3

        # 弾のリスト
        self.bullets = []

        self.key = key
        self.screen = screen

        self.key_list = {
            "right": pg.K_d,
            "left": pg.K_a,
            "up": pg.K_w,
            "down": pg.K_s,
            "fire": pg.K_SPACE
        }

    ## メソッド ##
    def get_hp(self):
        """メイン表示用にプレイヤーの体力を返す"""
        return self.player_hp
    
    def decrease_hp(self):
        """弾が当たったらプレイヤーの体力を1減らす"""
        self.player_hp -= 1

    def move_action(self):
        """キー入力に応じてキャラクターを移動させる"""
        
        # 画面の幅と高さを取得
        screen_width, screen_height = self.screen.get_size()

        # 画面外に出ないようにする
        # X座標を制限
        if self.player_pos.x < 0:
            self.player_pos.x = 0
        elif self.player_pos.x > screen_width - self.size:
            self.player_pos.x = screen_width - self.size

        # Y座標を制限
        if self.player_pos.y < 0:
            self.player_pos.y = 0
        elif self.player_pos.y > screen_height - self.size:
            self.player_pos.y = screen_height - self.size


                
        if self.key[self.key_list["right"]]:
            # 右向きキーが押された時、X座標を増やす
            self.player_pos.x += self.move_amount
            if self.fRight == False:
                # 右向きでなければ、左向きから右向きに変更
                self.img = pg.transform.flip(self.img, True, False)
                self.fRight = True
        
        if self.key[self.key_list["left"]]:
            # 左向きキーが押された時、X座標を減らす
            self.player_pos.x -= self.move_amount
            if self.fRight == True:
                # 左向きでなければ、右向きから左向きに変更
                self.img = pg.transform.flip(self.img, True, False)
                self.fRight = False

        if self.key[self.key_list["up"]]:
            # 上向きキーが押された時、Y座標を減らす
            self.player_pos.y -= self.move_amount

        if self.key[self.key_list["down"]]:
            # 下向きキーが押された時、Y座標を増やす
            self.player_pos.y += self.move_amount

        # # キャラクターを表示
        self.screen.blit(self.img, self.player_pos)

    # 弾を打つ
    def fire_bullet(self):
        """スペースキーが押された時に弾を発射する"""
        # TODO：未実装
        # ここでBulletクラスを呼び出して、self.bulletsの配列に追加する


    def update(self):
        """毎フレーム呼び出す処理"""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
        self.key = pg.key.get_pressed()
        self.move_action()
        self.screen.blit(self.img, self.player_pos)


class Octopus(Fish):
    def __init__(self, x, y, screen, key):
        super().__init__(x, y, screen, key)

        # 画像をタコに変更
        self.img = pg.image.load("images/fish_tako_oyogu.png")
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        # 右を向いているかどうかのフラグ
        self.fRight = False

        # キー設定を変更
        self.key_list = {
            "right": pg.K_RIGHT,
            "left": pg.K_LEFT,
            "up": pg.K_UP,
            "down": pg.K_DOWN,
            "fire": pg.K_KP_ENTER
        }
