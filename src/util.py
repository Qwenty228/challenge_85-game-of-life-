import random
from typing import Self, Literal
import pygame as pg
import pygame.freetype
import os


class Font:
    fonts = {}

    def __new__(cls, font=None, size=15) -> Self:

        if (font, size) not in cls.fonts:
            if font and os.path.exists(font):
                cls.fonts[(font, size)] = pg.freetype.Font(font, size)
            else:
                cls.fonts[(font, size)] = pg.freetype.SysFont(font, size)
        return cls.fonts[(font, size)]


def draw_text(win, text, font, color, x, y, align='center'):
    # print(text, font, color)
    text_surface, text_rect = font.render(text, color)
    if align == 'center':
        text_rect.center = (x, y)
    elif align == 'topleft':
        text_rect.topleft = (x, y)
    win.blit(text_surface, text_rect)

class Mouse:
    click = False
    unclick = False

    @staticmethod
    def reset():
        Mouse.click = False
        Mouse.unclick = False

    @staticmethod
    def map_pos(offset, tile_size):
        x, y = pg.mouse.get_pos()
        x = (x + offset[0]) // tile_size
        y = (y + offset[1]) // tile_size
        return x, y


class Button:
    def __init__(self, win, text, font, color, x, y, width, height, callback: callable=None):
        self.win = win
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback 
        self.rect = pg.Rect(x, y, width, height)
        self.clicked = False
        self.hovered = False

    def draw(self):
        color = self.color
        if self.hovered:
            color = (60, 80, 80)
        if Mouse.unclick and self.hovered:
            color = (50, 50, 50)
        pg.draw.rect(self.win, color, self.rect)
        draw_text(self.win, self.text, self.font, (0, 0, 0), self.x +
                  self.width//2, self.y + self.height//2, 'center')

    def update(self, mouse_pos: tuple=None):
        if not mouse_pos:
            mouse_pos = pg.mouse.get_pos()  
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered:
            if pg.mouse.get_pressed()[0]:
                self.clicked = Mouse.click
            if Mouse.unclick and self.callback:
                self.callback()
        else:
            self.clicked = False

    def is_active(self):
        return self.clicked