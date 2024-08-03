import pygame as pg
import pygame.gfxdraw



class GoL:
    _tile_size = 32
    def __init__(self, game, size, pos) -> None:
        self.size = size
        self.tile_size = game.map.tile_size
        self.pos = pos
        

        self.area = pg.Surface((size*self.tile_size, size*self.tile_size))
        self.area.fill((255, 255, 255))
        self.game = game

        pg.gfxdraw.rectangle(self.area, (0, 0, size*self.tile_size, size*self.tile_size), (255, 0, 0))
    
    def update(self) -> None:
        if self._tile_size != self.tile_size:
            self.area = pg.transform.scale(self.area, (self.size*self._tile_size, self.size*self._tile_size))
            self.tile_size = self._tile_size

    def draw(self, offset=(0, 0)):
        # draw if area is within the screen
        if self.pos[0]*self.tile_size - offset[0] < self.game.window.get_width() and self.pos[1]*self.tile_size - offset[1] < self.game.window.get_height():
            self.game.window.blit(self.area, (self.pos[0]*self.tile_size - offset[0], self.pos[1]*self.tile_size- offset[1]))
