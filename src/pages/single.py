import pygame as pg
import sys

from ..util import Mouse
from ..settings import WIDTH, HEIGHT
from .base import Page


class SinglePlayerPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.font = pg.font.Font(None, 74)
        self.window = pg.display.get_surface()

    def update(self):
        clock = pg.time.Clock()
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
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        Mouse.unclick = True
            
            dt = clock.tick(120) / 1000

            self.window.fill('white')

            text = self.font.render("Single Player", True, 'black' if not pg.mouse.get_pressed()[0] else 'red')
            self.window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

            pg.display.flip()

            if self._pause:
                result = self.pause_screen()
                if result == -1:
                    self.game.change_page("Main Menu")
                    break
            

