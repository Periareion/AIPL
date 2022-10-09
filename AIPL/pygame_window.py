
import pygame
import numpy as np

clock = pygame.time.Clock()


class Window:

    def __init__(self,
        title: str,
        size: tuple[int, int] = (600, 400),
        background_color: str = '#ffffff',
    ):
        width, height = size

        self.title = title
        self.width = width
        self.height = height
        self.background_color = background_color

        self.window_surface = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.reset()

    def mainloop(self):
        looping = True
        while looping:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    looping = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        pygame.image.save(self.window_surface, 'screenshot.png')

            clock.tick(60)

    def update(self):
        pygame.display.update()

    def reset(self):
        self.window_surface.fill(self.background_color)

    def render(self, obj, position=np.array((0,0))):
        obj.draw(self.window_surface, position)
        self.update()
