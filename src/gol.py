import pygame as pg
import pygame.gfxdraw
import numpy as np
import time

from .util import Mouse
from .settings import WIDTH, HEIGHT


class GoL:
    _tile_size = 32

    @classmethod
    def spawn(cls, game, size, pos):
        x1,y1,w1,h1 = *pos, size, size
        for gol in game.gameoflifes:
            x2, y2, w2, h2 = *gol.pos, gol.size, gol.size
            if not (x1 + w1 <= x2 or x1 >= x2 + w2 or y1 + h1 <= y2 or y1 >= y2 + h2):
                print('overlapped')
                return    
        game.gameoflifes.append(cls(game, size, pos))
            

    def __init__(self, game, size, pos) -> None:
        self.size = size
        self.tile_size = game.map.tile_size
        self.pos = list(pos)

        self.game = game

        self.area = pg.Surface((size*self.tile_size, size*self.tile_size), pg.SRCALPHA)
        self.area.fill((0,0,100))
        
        self.lock = False

        # draw grid 
        for x in range(0, size*self.tile_size, self.tile_size):
            pg.gfxdraw.vline(self.area, x, 0, size*self.tile_size, (0, 0, 0, 100))
        for y in range(0, size*self.tile_size, self.tile_size):
            pg.gfxdraw.hline(self.area, 0, size*self.tile_size, y, (0, 0, 0, 100))

        self.array = np.zeros((size, size, 4), dtype=np.int32)
    

    def update(self, cursor) -> None:
        if self._tile_size != self.tile_size:
            self.area = pg.transform.scale(self.area, (self.size*self._tile_size, self.size*self._tile_size))
            self.tile_size = self._tile_size
        
        if Mouse.click:
            x, y = cursor
            if x >= self.pos[0] and x < self.pos[0] + self.size and y >= self.pos[1] and y < self.pos[1] + self.size:
                if self.game.ui.current_tool == 'brush':    
                    # print(f"Clicked on {x}, {y}")
                    self.game.gol_array.array[y, x] = GoLArray.WHITE
                    # print(self.game.gol_array.array[self.pos[1]: self.pos[1] + self.size, self.pos[0]: self.pos[0] + self.size, 3])
                    self.lock = True
                
        if self.game.ui.current_tool != 'brush':
            self.lock = False
                
        self.array = self.game.gol_array.array[self.pos[1]:self.pos[1]+self.size, self.pos[0]:self.pos[0]+self.size, :]
        if np.sum(self.array[0, :, 3]) != 0:
            self.pos[1] -= 1
        if np.sum(self.array[-1, :, 3]) != 0:
            self.pos[1] += 1
        if np.sum(self.array[:, 0, 3]) != 0:
            self.pos[0] -= 1
        if np.sum(self.array[:, -1, 3]) != 0:
            self.pos[0] += 1
        


    def draw(self, offset=(0, 0)):
        # draw if area is within the screen
        left = offset[0]//self.tile_size
        right = (offset[0] + WIDTH)//self.tile_size + 1
        top = offset[1]//self.tile_size
        bottom = (offset[1] + HEIGHT)//self.tile_size  + 2

        if left < self.pos[0] + self.size < right and top < self.pos[1] + self.size < bottom:
            self.game.window.blit(self.area, (self.pos[0]*self.tile_size - offset[0], self.pos[1]*self.tile_size- offset[1]))
            for i in range(self.size):
                for j in range(self.size):
                    if self.array[i, j, 3] == 1:
                        pg.draw.rect(self.game.window, self.array[i, j, :3], (self.pos[0]*self.tile_size + j*self.tile_size - offset[0], self.pos[1]*self.tile_size + i*self.tile_size - offset[1], self.tile_size, self.tile_size))
          

class GoLArray:
    # rule 1, 3 die by underpopulation or overpopulation
    RED = np.array([70, 0, 0, 0], dtype=np.int32)
    WHITE = np.array([255, 255, 255, 1], dtype=np.int32)  # rule 2 live on
    GREEN = np.array([0, 55, 0, 1], dtype=np.int32)  # rule 4 new life
    BLACK = np.array([0, 0, 0, 0], dtype=np.int32)

    def __init__(self, game, size):
        self.game = game
        self.size = size

        self.array = np.zeros((size[1], size[0], 4), dtype=np.int32)

        self.running = True
        self.paused = False

    def update_full(self):
        new_board = self.array.copy()
        for i in range(self.array.shape[0]):
            for j in range(self.array.shape[1]):
                # Count the number of live neighbors
                n = np.sum(self.array[i-1:i+2, j-1:j+2, 3]
                           ) - self.array[i, j, 3]
                # Apply the rules of the game
                if self.array[i, j, 3] == 1 and n in [2, 3]:
                    new_board[i, j] = self.WHITE
                elif self.array[i, j, 3] == 1 and n not in [2, 3]:
                    new_board[i, j] = self.RED
                elif self.array[i, j, 3] == 0 and n == 3:
                    new_board[i, j] = self.GREEN
                else:
                    new_board[i, j] = self.BLACK
        self.array[:] = new_board

        
    def update_area(self):
        new_board = self.array.copy()
        for area in self.game.gameoflifes:
            # print(area.lock, area.pos)
            if area.lock: continue
            x, y = area.pos
            for i in range(y, y + area.size):
                for j in range(x, x + area.size):
                    # Count the number of live neighbors
                    n = np.sum(self.array[i-1:i+2, j-1:j+2, 3]
                               ) - self.array[i, j, 3]
                    # Apply the rules of the game
                    if self.array[i, j, 3] == 1 and n in [2, 3]:
                        new_board[i, j] = self.WHITE
                    elif self.array[i, j, 3] == 1 and n not in [2, 3]:
                        new_board[i, j] = self.RED
                    elif self.array[i, j, 3] == 0 and n == 3:
                        new_board[i, j] = self.GREEN
                    else:
                        new_board[i, j] = self.BLACK

        self.array[:] = new_board


    def daemon(self):
        while self.running:
            if not self.paused:
                self.update_area()
            time.sleep(0.5)
        print("Thread stopped")
            