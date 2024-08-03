import pygame as pg
import json



class Map:
    def __init__(self, game) -> None:
        self.game = game
        self.tile_size = 32
        self.tilemap = [] # [ {tiles layer}, {tiles layer}, ...]
        self.offgrid = {}

    @property
    def data(self):
        return {'tilemap': self.tilemap, 'offgrid': self.offgrid_tiles}
    
    def load(self, filename):
        if isinstance(filename, str):
            with open(filename, 'r') as f:
                data = json.load(f)
        elif isinstance(filename, dict):
            data = filename
        self.tilemap = data['tilemap']
        self.offgrid_tiles = data['offgrid']

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size,
                      'offgrid': self.offgrid_tiles}, f, indent=4)

        
    def render(self, surf, offset=(0, 0)):
        # for tile in self.offgrid_tiles:
        #     # usually are decorations, like trees, rocks, etc.
        #     surf.blit(self.game.assets[tile['type']][tile['variant']],
        #               (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        left = offset[0]//self.tile_size
        right = (offset[0] + surf.get_width())//self.tile_size + 1
        top = offset[1]//self.tile_size
        bottom = (offset[1] + surf.get_height())//self.tile_size + 1      

        for l, layer in enumerate(self.tilemap):
            for x in range(left, right):
                for y in range(top, bottom):
                    if f'{x};{y}' in layer:
                        tile = self.game.assets[layer[f'{x};{y}']['type']][layer[f'{x};{y}']['variant']]
                        surf.blit(tile, (x * self.tile_size - offset[0], y * self.tile_size - offset[1]))

if __name__ == "__main__":
    tilemap = [{}]
    for x in range(120):
        for y in range(60):
            if y in [0, 59] or x in [0, 119]:
                tilemap[0][f'{x};{y}'] = {'type': 'stone', 'variant': 0, 'pos': (x, y)}
                
            
    with open('map/1.json', 'w') as f:
        json.dump({'tilemap': tilemap, 'offgrid': []}, f, indent=4)