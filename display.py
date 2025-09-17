import pygame as pg


class Display:
    def __init__(self, screen, key):
        self.key = key
        self.screen = screen

    def update(self, hp1, hp2):
        # 画面を白で塗りつぶす
        self.screen.fill(pg.Color("GRAY"))

        # HP表示
        font = pg.font.SysFont(None, 50)
        text_surface = font.render(f"Player1 : {hp1}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (50, 50))

        text_surface = font.render(f"Player2 : {hp2}", True, pg.Color("BLACK"))
        self.screen.blit(text_surface, (450, 50))
