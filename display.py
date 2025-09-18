import pygame as pg


class Display:
    def __init__(self, screen, key):
        self.key = key
        self.screen = screen

        self.bg = pg.image.load("images/bg_natural_ocean.jpg")
        self.rect_bg = self.bg.get_rect()
        
        self.vs = pg.image.load("images/text_versus_vs.png")
        self.rect_vs = self.vs.get_rect()
        self.rect_vs.x = 570
        self.rect_vs.y = 10
        self.vs = pg.transform.scale(self.vs, (60, 60))

        self.player_list = []
    
    def add_player(self, player):
        self.player_list.append(player)

    def add_bullet(self, bullet):
        self.bullet_list.append(bullet)

    def update(self, hp1, hp2):
        # 背景表示
        self.screen.blit(self.bg, self.rect_bg)
        
        # 画面表示：VS, Player
        self.screen.blit(self.vs, self.rect_vs)
        
        font = pg.font.SysFont(None, 30)
        text_surface = font.render(f"Player 1", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (45, 65))
        text_surface = font.render(f"Player 2", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (1075, 65))

        # 当たり判定
        self.colliderect()
        
        # 終了判定
        if self.player_list[0].get_hp() < 1 or self.player_list[1].get_hp() < 1:
            return False

        # HP表示
        self.hp_bar()
        
        return True

    def colliderect(self):
        # プレイヤー同士の当たり判定
        if self.player_list[0].player_pos.colliderect(self.player_list[1].player_pos):
            if self.player_list[0].attack_now and not self.player_list[1].attack_now:
                # TODO ヒットストップ
                self.player_list[1].decrease_hp(self.player_list[0].attack_power)
                # TODO 無敵時間
                pass
            elif not self.player_list[0].attack_now and self.player_list[1].attack_now:
                # TODO ヒットストップ
                self.player_list[0].decrease_hp(self.player_list[1].attack_power)
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
        for bullet in self.player_list[0].bullets:
            if self.player_list[1].player_pos.colliderect(bullet.rect):
                self.player_list[1].decrease_hp(self.player_list[0].bullet_attack_power)
        for bullet in self.player_list[1].bullets:
            if self.player_list[0].player_pos.colliderect(bullet.rect):
                self.player_list[0].decrease_hp(self.player_list[1].bullet_attack_power)

    # HPのバーを表示する
    def hp_bar(self):
        player1_hp = int((self.player_list[0].player_hp / self.player_list[0].hp_max) * 496)
        
        pg.draw.rect(self.screen, (255,255,255), pg.Rect(40, 20, 500, 40))
        pg.draw.rect(self.screen, (80,80,80), pg.Rect(42, 22, 496, 36))
        pg.draw.rect(self.screen, (0,255,0), pg.Rect(538-player1_hp, 22, player1_hp, 36))
        
        player2_hp = int((self.player_list[1].player_hp / self.player_list[1].hp_max) * 496)
        
        pg.draw.rect(self.screen, (255,255,255), pg.Rect(660, 20, 500, 40))
        pg.draw.rect(self.screen, (80,80,80), pg.Rect(662, 22, 496, 36))
        pg.draw.rect(self.screen, (0,255,0), pg.Rect(662, 22, player2_hp, 36))
        
    
    # 開始画面
    def start_scene(self):
        # 背景表示
        self.screen.blit(self.bg, self.rect_bg)

        # タイトル表示
        font = pg.font.SysFont(None, 80)
        text_surface = font.render(f"Aqua Brawl", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 50))
        
        font = pg.font.SysFont(None, 80)
        text_surface = font.render(f"SPACE : Start", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 250))
    
    def game_scene(self):
        for i in range(3, 0, -1):
            # 背景表示
            self.screen.blit(self.bg, self.rect_bg)
            
            # キャラクター表示
            self.screen.blit(self.player_list[0].img, self.player_list[0].player_pos)
            self.screen.blit(self.player_list[1].img, self.player_list[1].player_pos)
            
            # カウントダウン表示
            font = pg.font.SysFont(None, 200)
            text_surface = font.render(f"{i}", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (550, 200))
            
            # 画面を更新
            pg.display.update()
            pg.time.Clock().tick(60)
            
            # 1秒待つ
            pg.time.delay(1000)
    
    # 終了画面
    def end_scene(self):
        # 背景表示
        self.screen.blit(self.bg, self.rect_bg)
        
        # 勝者表示
        font = pg.font.SysFont(None, 80)
        if self.player_list[0].get_hp() > self.player_list[1].get_hp():
            text_surface = font.render(f"Win Player1", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (50, 50))
        elif self.player_list[0].get_hp() < self.player_list[1].get_hp():
            text_surface = font.render(f"Win Player2", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (50, 50))
        else:
            text_surface = font.render(f"Draw", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (50, 50))

        # コンテニュー
        text_surface = font.render(f"CONTINUE? Y / N", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 200))
        