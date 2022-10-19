
import time

import pygame
import numpy as np

from . import utils


class Window:

    def __init__(self,
        title: str = 'Plot',
        size: tuple[int, int] = (600, 400),
        background_color: str = '#36393F',
    ):
        width, height = size

        self.title = title
        self.width = width
        self.height = height
        
        self.middle = width/2, height/2
        self.topleft = width/2, height/2

        self.background_color = background_color

        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.clear()
        
        self.last_loop_time = 0
        self.FPS = 60
        self.SPF = 1/self.FPS
        self.clock = pygame.time.Clock()


    def update(self):
        pygame.display.update()

    def clear(self):
        self.surface.fill(self.background_color)


    def mainloop_events(self, clear_surface=False, update_window=True, auto_quit=True):
        
        if (current_time := time.perf_counter()) - self.last_loop_time < self.SPF:
            return False
        pygame.display.set_caption(f'FPS: {round(1 / (current_time - self.last_loop_time), 2)}')
        self.last_loop_time = current_time
        
        if update_window:
            self.update()

        if clear_surface:
            self.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if auto_quit:
                    pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    image_name = utils.first_available_filename_number('screenshots/screenshot', '.png')
                    pygame.image.save(self.surface, image_name)

    def mainloop(self):
        looping = True
        while looping:
            looping = not bool(self.mainloop_events(auto_quit=False))
        pygame.quit()

    def render(self, obj, position=np.array((0,0)), update_window=True):
        obj.draw(self.surface, position)
