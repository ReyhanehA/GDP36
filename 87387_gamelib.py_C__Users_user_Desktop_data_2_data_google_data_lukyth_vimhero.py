import pygame
from pygame.locals import *

class SimpleGame(object):

    FPS = 60
    GAME_WIDTH = 640
    GAME_HEIGHT = 480

    def __init__(self,
                 title,
                 background_color,
                 window_size = (GAME_WIDTH,GAME_HEIGHT),
                 fps = FPS):
        self.title = title
        self.window_size = window_size
        self.fps = fps
        self.background_color = background_color

        self.is_terminated = False

    def __game_init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.title)
        self.font = pygame.font.SysFont("monospace", 20)

    def __handle_events(self):
        pass

    def terminate(self):
        self.is_terminated = True

    def run(self):
        self.init()
        while not self.is_terminated:
            self.__handle_events()

            self.update()

            self.surface.fill(self.background_color)
            self.render(self.surface)
            pygame.display.update()

            self.clock.tick(self.fps)

    def is_key_pressed(self, key):
        keys_pressed = pygame.key.get_pressed()
        if key < 0 or key >= len(keys_pressed):
            return False
        return (keys_pressed[key])

    def init(self):
        self.__game_init()

    def update(self):
        pass

    def render(self, surface):
        pass

    def on_key_up(self, key):
        pass

    def on_key_down(self, key):
        pass
