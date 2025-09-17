import pygame as pg


class Display:
    def __init__(self, screen, key):
        self.key = key
        self.screen = screen

        self.bg = pg.image.load("images/bg_natural_ocean.jpg")
        self.rect_bg = self.bg.get_rect()

        self.player_list = []
        self.bullet_list = []
        
        self.now_scene = 1 # 0:開始画面, 1:戦闘画面, 2:終了画面
    
    def add_player(self, player):
        self.player_list.append(player)

    def add_bullet(self, bullet):
        self.bullet_list.append(bullet)

    def update(self, hp1, hp2):
        # 背景表示
        self.screen.blit(self.bg, self.rect_bg)

        # 当たり判定
        self.colliderect()
        
        # 終了判定
        if self.player_list[0].get_hp() < 1 or self.player_list[1].get_hp() < 1:
            self.now_scene = 2

        # HP表示
        font = pg.font.SysFont(None, 50)
        text_surface = font.render(f"Player1 : {self.player_list[0].get_hp()}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 50))

        text_surface = font.render(f"Player2 : {self.player_list[1].get_hp()}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (900, 50))

    def colliderect(self):
        # プレイヤー同士の当たり判定
        if self.player_list[0].player_pos.colliderect(self.player_list[1].player_pos):
            if self.player_list[0].attack_now and not self.player_list[1].attack_now:
                # TODO ヒットストップ
                # TODO HP処理
                self.player_list[1].decrease_hp()
                # TODO 無敵時間
                pass
            elif not self.player_list[0].attack_now and self.player_list[1].attack_now:
                # TODO ヒットストップ
                self.player_list[0].decrease_hp()
                # TODO 無敵時間
                pass
            elif self.player_list[0].attack_now and self.player_list[1].attack_now:
                # とりあえずスルー
                # TODO 時間があったら、中心座標をつないだ線上に離れる
                # TODO 音付ける
                # self.player_list[0].decrease_hp()
                # self.player_list[1].decrease_hp()
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
            
    
    # 開始画面
    def start(self):
        # 背景表示
        self.screen.blit(self.bg, self.rect_bg)

        # タイトル表示
        font = pg.font.SysFont(None, 80)
        text_surface = font.render(f"魚格闘ゲーム", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 50))
        
        font = pg.font.SysFont(None, 50)
        text_surface = font.render(f"Player1 : {self.player_list[0].get_hp()}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 50))

        text_surface = font.render(f"Player2 : {self.player_list[0].get_hp()}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (900, 50))
    
    def game_scene(self):
        pass
    
    # 終了画面
    def end_scene(self):
        # 背景表示
        self.screen.blit(self.bg, self.rect_bg)
        
        # 勝者表示
        font = pg.font.SysFont(None, 80)
        if self.player_list[0].get_hp() > self.player_list[1].get_hp():
            text_surface = font.render(f"勝者：Player1", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (50, 50))
        elif self.player_list[0].get_hp() < self.player_list[1].get_hp():
            text_surface = font.render(f"勝者：Player2", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (50, 50))
        else:
            text_surface = font.render(f"引き分け", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (50, 50))

        # コンテニュー
        text_surface = font.render(f"CONTINUE? Y / N", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 200))
        