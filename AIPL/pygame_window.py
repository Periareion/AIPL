
import time

import pygame
import numpy as np

clock = pygame.time.Clock()


class Window:

    def __init__(self,
        title: str = 'Plot',
        size: tuple[int, int] = (600, 400),
        background_color: str = '#ffffff',
    ):
        width, height = size

        self.title = title
        self.width = width
        self.height = height
        
        self.middle = width/2, height/2
        self.topleft = width/2, height/2

        self.background_color = background_color

        self.window_surface = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.clear()
        
        self.last_loop_time = 0
        self.FPS = 60
        self.SPF = 1/self.FPS


    def update(self):
        pygame.display.update()

    def clear(self):
        self.window_surface.fill(self.background_color)


    def mainloop_events(self, clear_surface=False, update_window=True, auto_quit=True):
        
        if (current_time := time.perf_counter()) - self.last_loop_time < self.SPF:
            self.last_loop_time = current_time
            return False
        
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
                    pygame.image.save(self.window_surface, 'screenshot.png')

    def mainloop(self):
        looping = True
        while looping:
            looping = not bool(self.mainloop_events(auto_quit=False))
        pygame.quit()

    def render(self, obj, position=np.array((0,0)), update_window=True):
        obj.draw(self.window_surface, position)
