import pygame as pg
import pygame.gfxdraw

from .util import Mouse



class GoL:
    _tile_size = 32

    @classmethod
    def spawn(cls, game, size, pos):
        x1,y1,w1,h1 = *pos, size, size
        for gol in game.gameoflifes:
            x2, y2, w2, h2 = *gol.pos, gol.size, gol.size
            if not (x1 + w1 < x2 or x1 > x2 + w2 or y1 + h1 < y2 or y1 > y2 + h2):
                print('overlapped')
                return

        else:
            game.gameoflifes.append(cls(game, size, pos))
            

    def __init__(self, game, size, pos) -> None:
        self.size = size
        self.tile_size = game.map.tile_size
        self.pos = pos

        self.game = game

        self.area = pg.Surface((size*self.tile_size, size*self.tile_size), pg.SRCALPHA)
        self.area.fill((255, 255, 255))
        
        # draw grid 
        for x in range(0, size*self.tile_size, self.tile_size):
            pg.gfxdraw.vline(self.area, x, 0, size*self.tile_size, (0, 0, 0, 100))
        for y in range(0, size*self.tile_size, self.tile_size):
            pg.gfxdraw.hline(self.area, 0, size*self.tile_size, y, (0, 0, 0, 100))
    
    def update(self, cursor) -> None:
        if self._tile_size != self.tile_size:
            self.area = pg.transform.scale(self.area, (self.size*self._tile_size, self.size*self._tile_size))
            self.tile_size = self._tile_size
        
        if Mouse.click:
            x, y = cursor
            if x >= self.pos[0] and x < self.pos[0] + self.size and y >= self.pos[1] and y < self.pos[1] + self.size:
                if self.game.ui.current_tool == 'brush':    
                    print(f"Clicked on {x}, {y}")
                elif self.game.ui.current_tool == 'rectangle':
                    # print("spawn")
                    pass


    def draw(self, offset=(0, 0)):
        # draw if area is within the screen
        if self.pos[0]*self.tile_size - offset[0] < self.game.window.get_width() and self.pos[1]*self.tile_size - offset[1] < self.game.window.get_height():
            self.game.window.blit(self.area, (self.pos[0]*self.tile_size - offset[0], self.pos[1]*self.tile_size- offset[1]))
