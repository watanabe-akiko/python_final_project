import pygame as pg
from fish import Salmon,Shark,Hirame,Octopus,Squid,Robster

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
        
        self.title_logo = pg.image.load("images/logo.png")
        self.rect_title_logo = self.title_logo.get_rect()
        self.title_logo = pg.transform.scale(self.title_logo, (400, 200))

        self.player_list = []
        
        self.select1 = [2,0]
        self.select2 = [0,0]
        
        self.hirame = Hirame(0, 480, screen, pg.key.get_pressed(), 1)
        self.octopus = Octopus(1100, 480, screen, pg.key.get_pressed(), 2)
        self.salmon = Salmon(0, 480, screen, pg.key.get_pressed(), 1)
        self.shark = Shark(1100, 480, screen, pg.key.get_pressed(), 2)
        self.squid = Squid(0, 480, screen, pg.key.get_pressed(), 1)
        self.robster = Robster(1100, 480, screen, pg.key.get_pressed(), 2)

        self.result_logo = pg.image.load("images/result_logo.png")
        self.rect_result_logo = self.result_logo.get_rect()
        self.result_logo = pg.transform.scale(self.result_logo, (300, 200))

        self.winner_logo = pg.image.load("images/winner_logo.png")
        self.rect_winner_logo = self.winner_logo.get_rect()
        self.winner_logo = pg.transform.scale(self.winner_logo, (500, 400))

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
        text_surface = font.render(f"Player 1", True, pg.Color("BLUE"))
        self.screen.blit(text_surface, (45, 65))
        text_surface = font.render(f"Player 2", True, pg.Color("RED"))
        self.screen.blit(text_surface, (1075, 65))

        # 当たり判定
        self.colliderect()
        
        # 終了判定
        if self.player_list[0].get_hp() < 1 or self.player_list[1].get_hp() < 1:
            # 負けた時のエフェクト（2秒間アニメーション）
            defeat_time = pg.time.get_ticks()
            while True:
                # 背景再描画
                self.screen.blit(self.bg, self.rect_bg)
                # VS再描画
                self.screen.blit(self.vs, self.rect_vs)
                # HP再描画
                self.hp_bar()

                # プレイヤー再描画（エフェクト付き）
                if self.player_list[0].get_hp() < 1:
                    self.player_list[0].defeat_effect()
                else:
                    self.screen.blit(self.player_list[0].img, self.player_list[0].player_pos)
                if self.player_list[1].get_hp() < 1:
                    self.player_list[1].defeat_effect()
                else:
                    self.screen.blit(self.player_list[1].img, self.player_list[1].player_pos)

                pg.display.update()
                pg.time.Clock().tick(60)

                # 2秒経過したら結果表示
                if pg.time.get_ticks() - defeat_time > 2000:
                    break
            return False

        # HP表示
        self.hp_bar()
        
        return True

    def colliderect(self):
        # プレイヤー同士の当たり判定
        if self.player_list[0].player_pos.colliderect(self.player_list[1].player_pos):
            if self.player_list[0].attack_now and not self.player_list[1].attack_now:
                # 体当たり効果音を再生
                pg.mixer.Sound("sounds/maou_se_battle16.mp3").play()
                # ダメージ処理
                self.player_list[1].decrease_hp(self.player_list[0].attack_power)
                
                # ヒットストップ
                if self.player_list[1].player_hp > 0:
                    pg.time.delay(100)
                else:
                    pg.time.delay(500)
                
            elif not self.player_list[0].attack_now and self.player_list[1].attack_now:
                # 体当たり効果音を再生
                pg.mixer.Sound("sounds/maou_se_battle16.mp3").play()
                # ダメージ処理
                self.player_list[0].decrease_hp(self.player_list[1].attack_power)
                
                # ヒットストップ
                if self.player_list[0].player_hp > 0:
                    pg.time.delay(100)
                else:
                    pg.time.delay(500)
                
            elif self.player_list[0].attack_now and self.player_list[1].attack_now:
                # 体当たり効果音を再生
                pg.mixer.Sound("sounds/maou_se_battle16.mp3").play()
                # TODO 時間があったら、中心座標をつないだ線上に離れる
                # TODO 音付ける
                pass
            else:
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
        player1_hp_ratio = self.player_list[0].player_hp / self.player_list[0].hp_max
        player1_hp = int(player1_hp_ratio * 496)
        color1 = (0,255,0) if player1_hp_ratio > 0.3 else (255,0,0)
        
        pg.draw.rect(self.screen, (255,255,255), pg.Rect(40, 20, 500, 40))
        pg.draw.rect(self.screen, (80,80,80), pg.Rect(42, 22, 496, 36))
        pg.draw.rect(self.screen, color1, pg.Rect(538-player1_hp, 22, player1_hp, 36))

        player2_hp_ratio = self.player_list[1].player_hp / self.player_list[1].hp_max
        player2_hp = int(player2_hp_ratio * 496)
        color2 = (0,255,0) if player2_hp_ratio > 0.3 else (255,0,0)

        pg.draw.rect(self.screen, (255,255,255), pg.Rect(660, 20, 500, 40))
        pg.draw.rect(self.screen, (80,80,80), pg.Rect(662, 22, 496, 36))
        pg.draw.rect(self.screen, color2, pg.Rect(662, 22, player2_hp, 36))

    # 開始画面
    def start_scene(self):
        # 背景表示
        self.screen.blit(self.bg, self.rect_bg)

        # タイトル表示
        self.screen.blit(self.title_logo, (400, 20))
        
        # font = pg.font.SysFont(None, 80)
        # text_surface = font.render(f"SPACE : Start", True, pg.Color("BLACK"))
        # self.screen.blit(text_surface, (self.screen.get_width() // 2 - text_surface.get_width() // 2, 250))
        
        fish_list = []
        fish_list.append(self.hirame)
        fish_list.append(self.octopus)
        fish_list.append(self.salmon)
        fish_list.append(self.squid)
        fish_list.append(self.shark)
        fish_list.append(self.robster)
        
        for i, fish in enumerate(fish_list):
            # 画面表示、1行3匹
            self.screen.blit(fish.img, pg.Rect(200 + (i % 3 * 365), 250 + (i // 3) * 200, fish.img.get_width(), fish.img.get_height()))
        
        # プレイヤーごとに枠を表示、移動
        pg.draw.rect(self.screen, (255,0,0), pg.Rect(175 + (self.select1[0] % 3 * 365), 225 + (self.select1[1] * 200), 150, 150), 3)
        pg.draw.rect(self.screen, (0,0,255), pg.Rect(175 + (self.select2[0] % 3 * 365), 225 + (self.select2[1] * 200), 150, 150), 3)
        
        # キー入力
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    # select2の左移動
                    if self.select2[0] > 0:
                        self.select2[0] -= 1
                if event.key == pg.K_d:
                    # select2の右移動
                    if self.select2[0] < 2:
                        self.select2[0] += 1
                if event.key == pg.K_w:
                    # select2の上移動
                    if self.select2[1] > 0:
                        self.select2[1] -= 1
                if event.key == pg.K_s:
                    # select2の下移動
                    if self.select2[1] < 1:
                        self.select2[1] += 1
                if event.key == pg.K_LEFT:
                    # select1の左移動
                    if self.select1[0] > 0:
                        self.select1[0] -= 1
                if event.key == pg.K_RIGHT:
                    # select1の右移動
                    if self.select1[0] < 2:
                        self.select1[0] += 1
                if event.key == pg.K_UP:
                    # select1の上移動
                    if self.select1[1] > 0:
                        self.select1[1] -= 1
                if event.key == pg.K_DOWN:
                    # select1の下移動
                    if self.select1[1] < 1:
                        self.select1[1] += 1
                if event.key == pg.K_RETURN:
                    # 決定
                    player1_select = self.select1.copy()
                    player2_select = self.select2.copy()
                    return player1_select, player2_select
        return None, None

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

        # Resultロゴの表示
        self.screen.blit(self.result_logo, (10, -20))
        # winnerロゴの表示
        self.screen.blit(self.winner_logo, (380, -20))

        # 勝者表示
        font_win = pg.font.SysFont(None, 100)
        if self.player_list[0].get_hp() > self.player_list[1].get_hp():
            text_surface = font_win.render(f"Player1", True, pg.Color("BLUE"))
            self.screen.blit(text_surface, (500, 500))
            # 勝者の画像を表示
            winner = pg.transform.scale(self.player_list[0].img, (250, 250))
            self.screen.blit(winner, (500, 250))

        elif self.player_list[0].get_hp() < self.player_list[1].get_hp():
            text_surface = font_win.render(f"Player2", True, pg.Color("RED"))
            self.screen.blit(text_surface, (500, 500))
            # 勝者の画像を表示
            winner = pg.transform.scale(self.player_list[1].img, (250, 250))
            self.screen.blit(winner, (500, 250))
        else:
            text_surface = font_win.render(f"Draw", True, pg.Color("BLACK"))
            self.screen.blit(text_surface, (500, 500))

        # コンテニュー
        font_continue = pg.font.SysFont(None, 55)
        text_surface = font_continue.render(f"CONTINUE? Y / N", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (850, 600))
