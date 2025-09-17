import pygame as pg


class Display:
    def __init__(self, screen, key):
        self.key = key
        self.screen = screen

        self.bg = pg.image.load("images/bg_natural_ocean.jpg")
        self.rect_bg = self.bg.get_rect()

        self.player_list = []
        self.bullet_list = []

    def update(self, hp1, hp2):
        # 画面を白で塗りつぶす
        self.screen.fill(pg.Color("GRAY"))
        self.screen.blit(self.bg, self.rect_bg)

        # 当たり判定
        # self.colliderect()

        # HP表示
        font = pg.font.SysFont(None, 50)
        text_surface = font.render(f"Player1 : {hp1}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 50))

        text_surface = font.render(f"Player2 : {hp2}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (900, 50))

    def colliderect(self):
        # プレイヤー同士の当たり判定
        if self.player_list[0].colliderect(self.player_list[1]):
            if self.player_list[0] and not self.player_list[1]:
                # TODO ヒットストップ
                # TODO HP処理
                # TODO 無敵時間
                pass
            elif not self.player_list[0] and self.player_list[1]:
                # TODO ヒットストップ
                # TODO HP処理
                # TODO 無敵時間
                pass
            elif self.player_list[0] and self.player_list[1]:
                # とりあえずスルー
                # TODO 時間があったら、中心座標をつないだ線上に離れる
                # TODO 音付ける
                pass
            else:
                # とりあえずスルー
                # TODO 時間があったら、中心座標をつないだ線上に離れる
                # TODO 音付ける
                pass

        # 遠隔攻撃の当たり判定
        for player in self.player_list:
            for bullet in self.bullet_list:
                pass
