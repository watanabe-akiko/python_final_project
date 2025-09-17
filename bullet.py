#キー入力とblit以外をここにまとめる。
#移動メソッド、あたり判定のメソッドを作る。
# bullet.py
# キー入力とblit以外を定義する
import pygame as pg

class Bullet:
    def __init__(self, screen, player, x=810, y=-10):
        # 画像の読み込みとサイズ調整
        self.img = pg.image.load("images/glass_ball1_clear.png")
        self.size = 30
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        # 弾の位置（rect）
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.inframe = True

        # 移動速度
        self.speed = 10

        # 画面情報
        self.screen = screen

    def reset(self):
        """画面外の初期位置に戻す"""
        self.rect.x = 810
        self.rect.y = -10

    def fire(self, player_rect):
        """プレイヤー位置から弾を発射する"""
        self.rect.x = player_rect.x + 50 - 15 
        self.rect.y = player_rect.y

    def move_action(self):
        """弾の移動処理"""
        screen_width, screen_height = self.screen.get_size()
        if self.rect.x <= screen_width:
            self.rect.x += self.speed
            if self.rect.x > screen_width:
                self.inframe = False
            

    def check_hit(self, target_rect):
        """ターゲットとの当たり判定"""
        return self.rect.colliderect(target_rect)

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
        self.move_action()
        self.screen.blit(self.img, self.rect)