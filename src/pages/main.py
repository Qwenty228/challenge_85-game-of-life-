import pygame as pg
from .base import Page



class MainMenu(Page):
    def __init__(self, game):
        super().__init__(game)
        self.font = pg.font.Font(None, 74)
        self.buttons = {
            "Single Player": pg.Rect(300, 150, 200, 50),
            "Multiplayer": pg.Rect(300, 250, 200, 50),
            "Settings": pg.Rect(300, 350, 200, 50),
            "Quit": pg.Rect(300, 450, 200, 50),
        }
        self.window = pg.display.get_surface()

    def update(self):
        pass

    def draw(self):
        self.window.fill('white')
        for label, rect in self.buttons.items():
            pg.draw.rect(self.window, "blue", rect)
            text = self.font.render(label, True, 'white')
            self.window.blit(text, (rect.x + 10, rect.y + 10))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            for label, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    self.game.change_page(label)