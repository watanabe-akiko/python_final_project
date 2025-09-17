import pygame as pg
import sys
import random

from fish import Salmon,Shark,Hirame,Octopus,Squid,Robster
# from bullet import Bullet
from display import Display


# pygame初期化
pg.init()

# 画面設定
screen = pg.display.set_mode((1200, 676))

# 画面表示の追加
display = Display(screen, pg.key.get_pressed())

# キャラクター追加
fish1 = Salmon(0, 480, screen, pg.key.get_pressed(), 1)
fish2 = Shark(1100, 480, screen, pg.key.get_pressed(), 2) 

display.add_player(fish1)
display.add_player(fish2)

# 弾追加
# bullet = Bullet()

# 文字を表示するためのフォントを設定
font = pg.font.SysFont(None, 36)

while True:
    display.update(10, 20)

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
