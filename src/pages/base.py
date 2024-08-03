import pygame as pg

from ..util import Font, draw_text, Button, Mouse
from ..settings import WIDTH, HEIGHT


class Page:
    def __init__(self, game):
        self.game = game
        self._pause = False

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def handle_event(self, event):  # main game does not need to handle events
        # raise NotImplementedError
        pass
    
    def pause(self):
        self._pause = not self._pause
    
    def pause_screen(self):
        font1 = Font(None, 50)
        font2 = Font(None, 30)

        # self.win.blit(self.tint, (0, 0))
        tint = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        tint.fill((0, 0, 0, 100))

        curr = self.window.copy()
        curr.blit(tint, (0, 0))

        back = Button(self.window, 'Back', font2, (255, 255, 255),
                      WIDTH//2-80, HEIGHT*.3 + 175, 160, 50)
        title = Button(self.window, 'title', font1, (255, 255, 255),
                       WIDTH//2 - 80, HEIGHT*0.3 + 250, 160, 50)

        while True:
            Mouse.reset()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self._pause = False
                        return
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Mouse.click = True
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        Mouse.unclick = True

            self.window.blit(curr, (0, 0))
            draw_text(self.window, 'Paused', font1, 'white',
                      WIDTH//2, HEIGHT//2-50, 'center')
            draw_text(self.window, 'Press ESC to resume', font2,
                      'white', WIDTH//2, HEIGHT//2+50, 'center')
            back.update()
            back.draw()
            title.update()
            title.draw()

            pg.display.update()

            if back.is_active():
                self._pause = False
                return

            elif title.is_active():
                self._pause = False
                return -1