import pygame as pg
import sys

from fish import Salmon,Shark,Hirame,Octopus,Squid,Robster
from display import Display


# pygame初期化
pg.init()

# 画面設定
screen = pg.display.set_mode((1200, 676))
pg.display.set_caption("魚格闘ゲーム") 

# ゲーム起動
while True:
    # 初期設定
    # 画面表示の追加
    display = Display(screen, pg.key.get_pressed())
    # キャラクター追加
    fish1 = Salmon(0, 480, screen, pg.key.get_pressed(), 1)
    fish2 = Shark(1100, 480, screen, pg.key.get_pressed(), 2) 
    display.add_player(fish1)
    display.add_player(fish2)
    
    # スタート画面
    while True:
        # スペースで開始
        if pg.key.get_pressed()[pg.K_SPACE]:
            break
        
        # 背景表示
        display.start_scene()
        
        # 画面を更新
        pg.display.update()
        pg.time.Clock().tick(60)
        
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