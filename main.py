import pygame as pg
import sys

from fish import Salmon,Shark,Hirame,Octopus,Squid,Robster
from display import Display


# pygame初期化
pg.init()

# 画面設定
screen = pg.display.set_mode((1200, 676))
pg.display.set_caption("Aqua Brawl") 

# ゲーム起動
while True:
    # 初期設定
    # 画面表示の追加
    display = Display(screen, pg.key.get_pressed())
    
    # スタート画面
    while True:
        # スペースで開始
        # if pg.key.get_pressed()[pg.K_SPACE]:
        #     break
        
        # 背景表示
        player2_select, player1_select = display.start_scene()
        if player2_select is not None and player1_select is not None:
            if player2_select == [0,0]:
                fish2 = Hirame(1100, 480, screen, pg.key.get_pressed(), 2)
            elif player2_select == [1,0]:
                fish2 = Octopus(1100, 480, screen, pg.key.get_pressed(), 2)
            elif player2_select == [2,0]:
                fish2 = Salmon(1100, 480, screen, pg.key.get_pressed(), 2)
            elif player2_select == [0,1]:
                fish2 = Squid(1100, 480, screen, pg.key.get_pressed(), 2)
            elif player2_select == [1,1]:
                fish2 = Shark(1100, 480, screen, pg.key.get_pressed(), 2)
            elif player2_select == [2,1]:
                fish2 = Robster(1100, 480, screen, pg.key.get_pressed(), 2)
            if player1_select == [0,0]:
                fish1 = Hirame(0, 480, screen, pg.key.get_pressed(), 1)
            elif player1_select == [1,0]:
                fish1 = Octopus(0, 480, screen, pg.key.get_pressed(), 1)
            elif player1_select == [2,0]:
                fish1 = Salmon(0, 480, screen, pg.key.get_pressed(), 1)
            elif player1_select == [0,1]:
                fish1 = Squid(0, 480, screen, pg.key.get_pressed(), 1)
            elif player1_select == [1,1]:
                fish1 = Shark(0, 480, screen, pg.key.get_pressed(), 1)
            elif player1_select == [2,1]:
                fish1 = Robster(0, 480, screen, pg.key.get_pressed(), 1)
            # 選択されたキャラクターを追加
            display.add_player(fish1)
            display.add_player(fish2)
            break
        
        # 画面を更新
        pg.display.update()
        
        pg.time.Clock().tick(30)
        
        # イベントをチェック
        for event in pg.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
    
    # 遷移画面
    display.game_scene()

    # ゲームループ
    pg.mixer.music.load("sounds/maou_bgm_fantasy15.mp3")
    pg.mixer.music.play(-1)
    while True:
        live = display.update(10, 20)
        
        if not live:
            break

        # 魚をうごかす
        fish1.update()
        fish2.update() 

        # 画面を更新
        pg.display.update()

        pg.time.Clock().tick(60)

        # イベントをチェック
        for event in pg.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
    pg.mixer.music.stop()

    # エンド画面
    while True:
        display.end_scene()
        
        # yを押すと再スタート
        if pg.key.get_pressed()[pg.K_y]:
            break
        
        # nを押すと終了
        if pg.key.get_pressed()[pg.K_n]:
            pg.quit()
            sys.exit()
        
        # 画面を更新
        pg.display.update()
        pg.time.Clock().tick(60)
        
        # イベントをチェック
        for event in pg.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()