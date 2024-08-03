from ..settings import WIDTH, HEIGHT
from .base import Page

import pygame as pg


class SettingsPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.font = pg.font.Font(None, 74)
        self.window = pg.display.get_surface()  

    def update(self):
        pass

    def draw(self):
        self.window.fill('white')
        text = self.font.render("Settings", True, 'black')
        self.window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.change_page("Main Menu")