import pygame as pg
import sys

from ..util import Mouse
from ..settings import WIDTH, HEIGHT
from .base import Page
from ..map import Map


def gen_asset(name, n_var, color):
    variances = []
    for i in range(n_var):
        surface = pg.Surface((32, 32), pg.SRCALPHA)
        surface.fill(pg.Color(color).lerp(pg.Color('black'), i / n_var))
        variances.append(surface)
    return {name: variances}



class SinglePlayerPage(Page):
    def __init__(self, menu):
        super().__init__(menu)
        self.font = pg.font.Font(None, 74)
        self.window = pg.display.get_surface()


    def load_assets(self):
        self.assets = gen_asset('stone', 5, 'gray')
        self.map = Map(self)

        self.map.load("map/1.json")

    def update(self):
        
        clock = pg.time.Clock()
        self.load_assets()

        offset = [0, 0]

        while True:
            pg.display.set_caption(f"Single Player: {clock.get_fps():.2f}")
            Mouse.reset()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause()
                    if event.key == pg.K_F11:
                        pg.display.toggle_fullscreen()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Mouse.click = True
                        pg.mouse.get_rel() # clear rel
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        Mouse.unclick = True


            
            dt = clock.tick(120) / 1000

            if pg.mouse.get_pressed()[0]:
                dx, dy = pg.mouse.get_rel()
                offset[0] -= dx
                offset[1] -= dy
            self.window.fill('black')
            # self.window.fill('white')
            self.map.render(self.window, offset)
        

            pg.display.flip()

            if self._pause:
                result = self.pause_screen()
                if result == -1:
                    self.game.change_page("Main Menu")
                    break
            

