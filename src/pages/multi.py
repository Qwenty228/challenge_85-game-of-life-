import pygame as pg
import sys

from ..util import Mouse, Button, Font, draw_text
from ..settings import WIDTH, HEIGHT
from .base import Page
from .client import Client


class MultiplayerPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.font = pg.font.Font(None, 74)
        self.window = pg.display.get_surface()

        self.buttons = [
            Button(self.window, "Back", Font(size=15), (100, 100, 120), 25, 25, 100, 50, self.game.change_page),
            Button(self.window, "Join", Font(size=15), (100, 100, 120),  WIDTH/2 - 150, HEIGHT / 2, 100, 50, self.join),
            Button(self.window, "Host", Font(size=15), (100, 100, 120),  WIDTH/2 + 50, HEIGHT / 2, 100, 50, self.host)
        ]

    def join(self):
        print("Joining")
        Client(self.game, 'join').update()

    def host(self):
        print("Hosting")
        Client(self.game, 'host').update()

    def update(self):
        for button in self.buttons:
            button.update()


    def draw(self):
        self.window.fill('gray20')
        for button in self.buttons:
            button.draw()

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.change_page("Main Menu")