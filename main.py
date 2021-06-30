import numpy as np
import pygame as pg


pg.init()

WIN_SIZE = (1280, 640)
cols, rows = 160, 80

def make2darray(cols, rows):
    return [[1 if np.random.uniform(0, 1) > 0.5 else 0 for x in range(cols)] for y in range(rows)]
    
def draw_grid(cols, rows, content):
    width = WIN_SIZE[0]//cols
    height = WIN_SIZE[1]//rows
    for y in range(rows):
        for x in range(cols):
            if content[y][x] == 1:
                pg.draw.rect(SURFACE, (255,255,255), pg.Rect(x*width , y*height, width-1, height-1))
    '''for y in range(rows):
        pg.draw.line(SURFACE, 'black',(0, (y+1)*height), (WIN_SIZE[0],(y+1)*height ), 2)
    for x in range(cols):
        pg.draw.line(SURFACE, 'black',((x+1)*width, 0), ((x+1)*width, WIN_SIZE[1]), 2)'''

    
def grid_cal(grid):
    #Ret = []
    check = []
    next_grid = grid[:]
    for y in range(rows):
        #Ret.append([])
        for x in range(cols):
            sum_nn = 0
            for near_col in [-1,0,1]:
                for near_row in [-1,0,1]:
                    #if 0 <= y + near_row < len(grid) and 0 <= x + near_col < len(grid[0]):
                    sum_nn += grid[(y + near_row + rows) % rows][(x + near_col + cols) % cols] 
            sum_nn -= grid[y][x]
            state = grid[y][x]
            if (state==0 and sum_nn == 3):
                #Ret[y].append(f'row: {y} and col: {x} has sum neighbor = {sum_nn} and state = {state}')
                check.append([y,x,1])
                #next_grid[y][x] = 1
                
            elif (state == 1 and sum_nn < 2) or (state==1 and sum_nn >3):
                #Ret[y].append(f'row: {y} and col: {x} has sum neighbor = {sum_nn} and state = {state}')
                check.append([y,x,0])
                #next_grid[y][x] = 0
            else:
                next_grid[y][x] = grid[y][x]
            #Ret[y].append(f'row: {y} and col: {x} has sum neighbor = {sum_nn} and state = {state}')
    if len(check) > 0:
        for state in check:
            next_grid[state[0]][state[1]] = state[2]

    return next_grid

            
    
    


grid = make2darray(cols, rows)

CLOCK = pg.time.Clock()
FPS = 120
SURFACE = pg.display.set_mode(WIN_SIZE)
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                grid = make2darray(cols, rows)
            if event.key == pg.K_a:
                pass
    grid = grid_cal(grid)
                
            
    SURFACE.fill('black')
    draw_grid(cols, rows, grid)

    

    pg.display.update()
    CLOCK.tick(FPS)
pg.quit()
