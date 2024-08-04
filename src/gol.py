import pygame as pg
import pygame.gfxdraw
import numpy as np
import time

from .util import Mouse
from .settings import WIDTH, HEIGHT, MOVEMENT_INDICATOR


class GoL:
    _tile_size = 32

    @classmethod
    def spawn(cls, game, size, pos, gameoflifes):
        if isinstance(size, int):
            size = size, size

        x1, y1, w1, h1 = *pos, *size
        for gol in gameoflifes:
            x2, y2, w2, h2 = *gol.pos, *gol.size
            if not (x1 + w1 <= x2 or x1 >= x2 + w2 or y1 + h1 <= y2 or y1 >= y2 + h2):
                print('overlapped')
                return
        cls.gameoflifes = gameoflifes
        cls.gameoflifes.append(cls(game, size, pos))
        

    def __init__(self, game, size, pos) -> None:
        self.size = size
        if isinstance(size, int):
            self.size = size, size
        self.tile_size = game.map.tile_size
        self.pos = list(pos)

        self.game = game

        self.area = pg.Surface(
            (self.size[0]*self.tile_size, self.size[1]*self.tile_size), pg.SRCALPHA)
        self.area.fill((0, 0, 100))

        self.lock = False
        self.dead = False

        # draw grid
        for x in range(0, self.size[0]*self.tile_size, self.tile_size):
            pg.gfxdraw.vline(
                self.area, x, 0, self.size[1]*self.tile_size, (0, 0, 0, 100))
        for y in range(0, self.size[1]*self.tile_size, self.tile_size):
            pg.gfxdraw.hline(
                self.area, 0, self.size[0]*self.tile_size, y, (0, 0, 0, 100))

        self.array = np.zeros((*self.size, 4), dtype=np.int32)

        self.movelimit = 0

    def upsize(self, size, pos):
        self.pos = list(pos)
        self.size = size
        if isinstance(size, int):
            self.size = size, size
        self.area = pg.Surface(
            (self.size[0]*self.tile_size, self.size[1]*self.tile_size), pg.SRCALPHA)
        self.area.fill((0, 0, 100))

        # draw grid
        for x in range(0, self.size[0]*self.tile_size, self.tile_size):
            pg.gfxdraw.vline(
                self.area, x, 0, self.size[1]*self.tile_size, (0, 0, 0, 100))
        for y in range(0, self.size[1]*self.tile_size, self.tile_size):
            pg.gfxdraw.hline(
                self.area, 0, self.size[0]*self.tile_size, y, (0, 0, 0, 100))

        self.array = np.zeros((*self.size, 4), dtype=np.int32)

    def update(self, cursor) -> None:
        if self._tile_size != self.tile_size:
            self.area = pg.transform.scale(
                self.area, (self.size[0]*self._tile_size, self.size[1]*self._tile_size))
            self.tile_size = self._tile_size

        if Mouse.click:
            x, y = cursor
            if x >= self.pos[0] and x < self.pos[0] + self.size[0] and y >= self.pos[1] and y < self.pos[1] + self.size[1]:
                if self.game.ui.current_tool == 'brush':
                    # print(f"Clicked on {x}, {y}")
                    self.game.gol_array.array[y, x] = GoLArray.WHITE
                    # print(self.game.gol_array.array[self.pos[1]: self.pos[1] + self.size, self.pos[0]: self.pos[0] + self.size, 3])
                    self.lock = True

        self.array = self.game.gol_array.array[self.pos[1]:self.pos[1] +
                                            self.size[1], self.pos[0]:self.pos[0]+self.size[0], :]   # for drawing
                                            

        if self.game.ui.current_tool != 'brush':
            self.lock = False
        

    def draw(self, offset=(0, 0)):
        # draw if area is within the screen
        left = offset[0]//self.tile_size
        right = (offset[0] + WIDTH)//self.tile_size
        top = offset[1]//self.tile_size
        bottom = (offset[1] + HEIGHT)//self.tile_size

        if left - self.size[0] < self.pos[0] < right and top - self.size[1] < self.pos[1] < bottom:
            self.game.window.blit(
                self.area, (self.pos[0]*self.tile_size - offset[0], self.pos[1]*self.tile_size - offset[1]))
            for i in range(self.size[1]):
                for j in range(self.size[0]):
                    if self.array[i, j, 3] == 1:
                        pg.draw.rect(self.game.window, self.array[i, j, :3], (self.pos[0]*self.tile_size + j*self.tile_size -
                                     offset[0], self.pos[1]*self.tile_size + i*self.tile_size - offset[1], self.tile_size, self.tile_size))


class GoLArray:
    # rule 1, 3 die by underpopulation or overpopulation
    RED = np.array([70, 0, 0, 0], dtype=np.int32)
    WHITE = np.array([255, 255, 255, 1], dtype=np.int32)  # rule 2 live on
    GREEN = np.array([0, 55, 0, 1], dtype=np.int32)  # rule 4 new life
    BLACK = np.array([0, 0, 0, 0], dtype=np.int32)

    def __init__(self, game, size, gameoflifes) -> None:
        self.game = game
        self.size = size
        self.gameoflifes = gameoflifes

        self.array = np.zeros((size[1], size[0], 4), dtype=np.int32)

        self.running = True
        self.paused = False
        self.updating = True
       

        self.prev_data = {}

    def update_area(self):
        
        new_board = self.array.copy()
        for area in self.gameoflifes:
            # print(area.lock, area.pos)
            if area.lock:
                continue
            x, y = area.pos
            w, h = area.size
            prev_array = self.array[y:y+h, x:x+w, 3].copy()
            for i in range(y, y + area.size[1]):
                for j in range(x, x + area.size[0]):
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
   
            # Process the result, same interval as gol_array thread
            array = new_board[y:y+h, x:x+w, 3]
            
            if np.sum(array[0, :]) != 0 and np.sum(array[-2, :]) == 0 and area.pos[1] > 1:
                area.pos[1] -= 1
            if np.sum(array[-1, :]) != 0 and np.sum(array[1, :]) == 0 and area.pos[1] + area.size[1] < self.size[1] - 1:
                area.pos[1] += 1
            if np.sum(array[:, 0]) != 0 and np.sum(array[:, -2]) == 0 and area.pos[0] > 1:
                area.pos[0] -= 1
            if np.sum(array[:, -1]) != 0 and np.sum(array[:, 1]) == 0 and area.pos[0] + area.size[0] < self.size[0] - 1:
                area.pos[0] += 1

            if self.prev_data[area] == area.pos:
                area.movelimit += 1
            else:
                area.movelimit = 0  # if moving, it cannot generate energy
            if area.movelimit >= MOVEMENT_INDICATOR:   # every 5 interval, calculate energy
                # Create a mask of positions where array2 has 1s
                array2_ones = (array == 1)
                
                # Create a mask of positions where array1 has 1s
                array1_ones = (prev_array == 1)
                
                # Find positions where array2 has 1s and array1 does not have 1s
                different_ones = array2_ones & ~array1_ones
                
                # Count the number of different 1s
                self.game.generate_energy(np.sum(different_ones))

                area.movelimit = 0

           
      
        self.array[:] = new_board
        

      
    def fuse_area(self):
        dead = []
        for i, area1 in enumerate(self.gameoflifes):
            if area1.dead:
                continue
            for area2 in self.gameoflifes[i+1:]:
                if area2.dead:
                    continue
                x1, y1 = area1.pos
                x2, y2 = area2.pos
                if not (x1 + area1.size[0] < x2 or x1 > x2 + area2.size[0] or y1 + area1.size[1] < y2 or y1 > y2 + area2.size[1]):
                    area2.dead = True
                    dead.append(area2)
                    x = min(x1, x2)
                    y = min(y1, y2)
                    size = max(x1 + area1.size[0], x2 + area2.size[0]) - \
                        x, max(y1 + area1.size[1], y2 + area2.size[1]) - y
                    area1.upsize(size, (x, y))

        for area in self.gameoflifes:
            if area.dead:
                self.gameoflifes.remove(area)
                if area in self.prev_data:
                    del self.prev_data[area]
                del area
                continue

            if not area.lock:
                self.prev_data[area] = area.pos.copy()
        

    def daemon(self):
        while self.running:
            if not self.paused and self.gameoflifes:
                self.fuse_area()
                self.update_area()
       
          
            time.sleep(0.2)            

        print("Thread stopped")
