import pygame as pg

from .util import Font, draw_text, Button, Mouse
from .settings import WIDTH, HEIGHT


class UI:
    def __init__(self, game, rect) -> None:
        self.game = game
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size)

        self.image.fill('gray10')

        self.current_tool = None
        self.rect_start_pos = None

        # Define buttons
        self.buttons = [Button(self.image, "area", Font(size=15), 'gray40', 10, 10, self.rect.h*0.8, self.rect.h*0.8, self.select_rectangle_tool),
                        Button(self.image, "draw", Font(size=15), 'gray40', 20 + self.rect.h*0.8, 10, self.rect.h*0.8, self.rect.h*0.8, self.select_brush_tool),
                        Button(self.image, "move", Font(size=15), 'gray40', 30 + 2*self.rect.h*0.8, 10, self.rect.h*0.8, self.rect.h*0.8, self.deselect)]

    def select_rectangle_tool(self):
        self.current_tool = 'rectangle'
        print(f"Selected tool: {self.current_tool}")

    def select_brush_tool(self):
        self.current_tool = 'brush'
        print(f"Selected tool: {self.current_tool}")

    def deselect(self):
        self.current_tool = None
        print(f"Deselected tool")


    def draw(self):
        x, y = pg.mouse.get_pos()
        x -= self.rect.x
        y -= self.rect.y

        for button in self.buttons:
            button.update((x, y))
            button.draw()
        self.game.window.blit(self.image, self.rect)
