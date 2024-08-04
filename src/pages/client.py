"""
Client for multiplayer game
2 players can play the game
"""
import threading
import pygame as pg
import sys
import random

from ..util import Mouse
from ..settings import *
from .base import Page
from ..map import Map
from ..gol import GoL, GoLArray
from ..ui import UI
from ..server import Network, stop_server, start_server


def gen_asset(name, n_var, color, size=32):
    variances = []
    for i in range(n_var):
        surface = pg.Surface((size, size), pg.SRCALPHA)
        surface.fill(pg.Color(color).lerp(pg.Color('black'), i / n_var))
        variances.append(surface)
    return {name: variances}


class Client(Page):
    def __init__(self, menu, type='host'):
        super().__init__(menu)
        self.window = pg.display.get_surface()
        if type == 'host':
            threading.Thread(target=start_server).start()
            self.network = None
        else:
            self.network = Network()
            self.network.connect()

    def load_assets(self):
        self.assets = gen_asset('stone', 5, 'gray')
        self.map = Map(self)

        self.map.load("map/1.json")
        self.gameoflifes = []

        self.gol_array = GoLArray(self, (map_w, map_h), self.gameoflifes)

        self.ui = UI(self, (0, 0.8*HEIGHT, WIDTH, 0.2*HEIGHT))

        self.energy = 50

        self.heart = None

    def update_assets_size(self, size):
        self.assets.update(gen_asset('stone', 5, 'gray', size))

    def camera(self, offset, is_zoomable):
        if pg.mouse.get_pressed()[0] and self.ui.current_tool == 'move':       # move map
            dx, dy = pg.mouse.get_rel()
            offset[0] -= dx
            offset[1] -= dy

        if offset[1] < 0:
            offset[1] = 0
        elif offset[1] > map_h * self.map.tile_size - HEIGHT + self.ui.rect.h:
            offset[1] = map_h * self.map.tile_size - HEIGHT + self.ui.rect.h
        if offset[0] < 0:
            offset[0] = 0
        elif offset[0] > map_w * self.map.tile_size - WIDTH:
            offset[0] = map_w * self.map.tile_size - WIDTH

        if map_w * self.map.tile_size < WIDTH:
            is_zoomable = False
            offset[0] = (map_w * self.map.tile_size - WIDTH) // 2
        if map_h * self.map.tile_size < HEIGHT - self.ui.rect.h:
            is_zoomable = False
            offset[1] = (map_h * self.map.tile_size - HEIGHT + self.ui.rect.h) // 2

        return offset, is_zoomable

    
    def generate_energy(self, n_energy):
        self.energy += n_energy
        
    
    def update(self):

        clock = pg.time.Clock()
        self.load_assets()

        offset = [0, 0]
        is_zoomable = True

        computation_thread = threading.Thread(target=self.gol_array.daemon)
        computation_thread.daemon = True  # Allow the thread to exit when the main program exits
        computation_thread.start()

        self.heart = GoL.spawn(self, 5, (2, random.randint(2, map_h-7)), self.gameoflifes, True) # spawn GoL

        while True:
            pg.display.set_caption(f"Single Player: {clock.get_fps():.2f}")
            Mouse.reset()
            offset, is_zoomable = self.camera(offset, is_zoomable)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause()
                    if event.key == pg.K_F11:
                        pg.display.toggle_fullscreen()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Mouse.click = True
                        pg.mouse.get_rel()  # clear rel
                    if event.button == 4:
                        self.map.tile_size *= 2
                        self.update_assets_size(self.map.tile_size)
                        is_zoomable = True
                        GoL._tile_size = self.map.tile_size

                    elif event.button == 5:
                        if is_zoomable:
                            self.map.tile_size //= 2
                            self.update_assets_size(self.map.tile_size)
                            GoL._tile_size = self.map.tile_size

                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        Mouse.unclick = True

            clock.tick(120)

            if Mouse.click and not self.ui.rect.collidepoint(pg.mouse.get_pos()) and self.ui.current_tool == 'area':            
                x, y = Mouse.map_pos(offset, self.map.tile_size)
                if x > 0 and y > 0 and x < map_w - self.ui.area_size + 1 and y < map_h - self.ui.area_size + 1:
                                  
                    GoL.spawn(self, self.ui.area_size, (x, y), self.gameoflifes) # spawn GoL
                    
                        
                            
                   

            self.window.fill('black')
            
            self.map.render(self.window, offset)
            

            for gol in self.gameoflifes:
                gol.update(Mouse.map_pos(offset, self.map.tile_size))
                gol.draw(offset)
               
            # draw grid
            # max(0, left) * self.tile_size - offset[0], max(0, top)*self.tile_size - offset[1], middle * self.tile_size, min(map_h, bottom)* self.tile_size)
            if self.map.tile_size > 8:
                for x in range(max(offset[0]//self.map.tile_size, 0), min(map_w, offset[0]//self.map.tile_size + WIDTH//self.map.tile_size + 1)):
                    pg.gfxdraw.vline(self.window, x*self.map.tile_size - offset[0], 0, HEIGHT, (75, 75, 75))
                for y in range(max(offset[1]//self.map.tile_size, 0), min(map_h, offset[1]//self.map.tile_size + HEIGHT//self.map.tile_size + 1)):
                    pg.gfxdraw.hline(self.window, 0, WIDTH, y*self.map.tile_size - offset[1], (75, 75, 75))
                
                    

            self.ui.draw()

            pg.display.flip()

            if self.heart == 'dead':
                break

            if self._pause:
                result = self.pause_screen()
                if result == -1:
                    break
        if not self.network:
            print("Stopping server")
            stop_server()
        else:
            self.network.client.close()

        self.game.change_page("Main Menu")
        self.gol_array.running = False
        