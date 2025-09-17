import pygame as pg
from bullet import Bullet
# from bullet import Bullet # 弾クラスをインポート

# ボタン押しながら
class Fish:
    def __init__(self, x, y, screen, key, player):
        self.img = pg.image.load("images/fish_sakana_sake.png")
        self.size = 100
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        self.player_pos = self.img.get_rect()  # 画像の矩形情報(player_rect)を取得
        self.player_pos.x = x
        self.player_pos.y = y
        
        # 体当たり判定のフラグ
        self.attack_now = False
        self.attack_start_time = 0
        # 移動量
        self.move_amount = 10

        # 体力
        self.player_hp = 3

        # 弾のリスト
        self.bullets = []

        self.key = key
        self.screen = screen
        self.player = player
        self.mouth = 35

        if player == 1:
            # 右を向いているかどうかのフラグ
            self.fRight = True

        self.key_list = {
            "right": pg.K_d,
            "left": pg.K_a,
            "up": pg.K_w,
            "down": pg.K_s,
            "fire": pg.K_SPACE,
            "attack": pg.K_b
        }

        if player == 2:
            # 右を向いているかどうかのフラグ
            self.fRight = False

            # キー設定を変更
            self.key_list = {
                "right": pg.K_RIGHT,
                "left": pg.K_LEFT,
                "up": pg.K_UP,
                "down": pg.K_DOWN,
                "fire": pg.K_BACKSPACE,
                "attack": pg.K_RSHIFT
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

    # 体当たりを行う
    def attack(self):
        """攻撃キーが押された時に体当たりを行う"""
        # 攻撃キーが押された時の時間を取得
        now = pg.time.get_ticks()

        if self.key[self.key_list["attack"]] and self.attack_now == False:
            # どの方向に体当たりするか決定
            if self.key[self.key_list["right"]]:
                self.attack_direction = "right"
            elif self.key[self.key_list["left"]]:
                self.attack_direction = "left"
            elif self.key[self.key_list["up"]]:
                self.attack_direction = "up"
            elif self.key[self.key_list["down"]]:
                self.attack_direction = "down"
            else:
                self.attack_direction = None

            if self.attack_direction:
                self.attack_now = True
                self.attack_start_time = now

        if self.attack_now == True:
            # 攻撃中、最初に押した方向キーの方向にスピードアップ
            if self.attack_direction == "right":
                self.player_pos.x += self.move_amount * 2
            elif self.attack_direction == "left":
                self.player_pos.x -= self.move_amount * 2
            elif self.attack_direction == "up":
                self.player_pos.y -= self.move_amount * 2
            elif self.attack_direction == "down":
                self.player_pos.y += self.move_amount * 2

        # 1秒経ったら体当たり終了
        if now - self.attack_start_time >= 100: #100ミリ秒
            self.attack_now = False


    # 弾を打つ
    def fire_bullet(self):
        if self.key[self.key_list["fire"]]:
            bullet = Bullet(self.screen, self.player)
            bullet.fire(self.player_pos, self.mouth, self.fRight)
            self.bullets.append(bullet)
        for bul in self.bullets:
            flag = bul.move_action()
            self.screen.blit(bul.img, bul.rect)
        del_index = [] 
        for bul in self.bullets:   
            if bul.inframe == False:
                del_index.append(bul)
        self.bullets = [i for i in self.bullets if not i in del_index]      
            
        


    def update(self):
        """毎フレーム呼び出す処理"""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
        self.key = pg.key.get_pressed()
        self.move_action()
        self.attack()
        self.fire_bullet()
        self.screen.blit(self.img, self.player_pos)

# サーモンクラス
class Salmon(Fish):
    def __init__(self, x, y, screen, key, player):
        super().__init__(x, y, screen, key, player)

        # 画像をサーモンに変更
        self.img = pg.image.load("images/fish_sakana_sake.png")
        self.img = pg.transform.scale(self.img, (self.size, self.size))
        
        # 1Pであれば画像を左右反転
        if player == 1:
            self.img = pg.transform.flip(self.img, True, False)

class Shark(Fish):
    def __init__(self, x, y, screen, key, player):
        super().__init__(x, y, screen, key, player)
        
        # 画像をサメに変更
        self.img = pg.image.load("images/kodai_megalodon.png")
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        # 1Pであれば画像を左右反転
        if player == 1:
            self.img = pg.transform.flip(self.img, True, False)
            
        #口の位置
        self.mouth = 60


class Hirame(Fish):
    def __init__(self, x, y, screen, key, player):
        super().__init__(x, y, screen, key, player)
        
        # 画像をヒラメに変更
        self.img = pg.image.load("images/fish_sakana_hirame.png")
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        # 1Pであれば画像を左右反転
        if player == 1:
            self.img = pg.transform.flip(self.img, True, False)


# タコクラス
class Octopus(Fish):
    def __init__(self, x, y, screen, key, player):
        super().__init__(x, y, screen, key, player)

        # 画像をタコに変更
        self.img = pg.image.load("images/fish_tako_oyogu.png")
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        # 1Pであれば画像を左右反転
        if player == 1:
            self.img = pg.transform.flip(self.img, True, False)
            
        #口の位置
        self.mouth = 50

# イカ
class Squid(Fish):
    def __init__(self, x, y, screen, key, player):
        super().__init__(x, y, screen, key, player)
        # 画像をタコに変更
        self.img = pg.image.load("images/fish_sakana_yariika_syokuwan.png")
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        # 1Pであれば画像を左右反転
        if player == 1:
            self.img = pg.transform.flip(self.img, True, False)


# ロブスター
class Robster(Fish):
    def __init__(self, x, y, screen, key, player):
        super().__init__(x, y, screen, key, player)
        # 画像をロブスターに変更
        self.img = pg.image.load("images/fish_lobster.png")
        self.img = pg.transform.scale(self.img, (self.size, self.size))

        # 1Pであれば画像を左右反転
        if player == 1:
            self.img = pg.transform.flip(self.img, True, False)

