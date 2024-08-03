import pygame as pg
import sys

from src.util import Mouse
from src.settings import SIZE
from src.pages import MainMenu, SettingsPage, SinglePlayerPage, MultiplayerPage

# Initialize Pygame
pg.init()

# Screen dimensions

# Set up the screen
screen = pg.display.set_mode(SIZE, pg.SCALED)
pg.display.set_caption("Page Navigator Example")




class Game:
    def __init__(self):
        self.pages = {
            "Main Menu": MainMenu(self),
            "Settings": SettingsPage(self),
            "Single Player": SinglePlayerPage(self),
            "Multiplayer": MultiplayerPage(self)
        }
        self.current_page = "Main Menu"

    def change_page(self, page_name):
        if page_name.lower().strip() == "quit":
            pg.quit()
            sys.exit()
        if page_name in self.pages:
            self.current_page = page_name
            if page_name == "Main Menu":
                pg.display.set_caption("Page Navigator Example")

    def run(self):
        clock = pg.time.Clock()
        while True:
            Mouse.reset()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.pages[self.current_page].handle_event(event)

            self.pages[self.current_page].update()
            self.pages[self.current_page].draw()

            pg.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()
