import pygame
from pygame.locals import *

import gamelib
from elements import Arrow
from elements import Text

class MainGame(gamelib.SimpleGame):
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    SECOND = 1000
    
    def __init__(self):
        super(MainGame, self).__init__('VimHero', MainGame.BLACK)
        self.instruction = []
        self.arrow = Arrow(pos = (self.window_size[0] / 2, self.window_size[1] / 2))
        x = self.window_size[0] / 20
        y = self.window_size[1]
        self.create_instruction("h : left", (x, y - 120), MainGame.WHITE, self.font)
#        self.create_instruction("j : up", (x, y - 100), MainGame.WHITE, self.font)
#        self.create_instruction("k : down", (x, y - 80), MainGame.WHITE, self.font)
#        self.create_instruction("l : right", (x, y - 60), MainGame.WHITE, self.font)
#        self.create_instruction("Spacebar : Restart", (x, y - 40), MainGame.WHITE, self.font)
#        self.create_instruction("ESC : Exit", (x, y - 20), MainGame.WHITE, self.font)
        self.init_game()

    def create_instruction(self, text, pos, color, font):
        self.instruction.append(Text(text, pos, color, font))
        
    def init(self):
        super(MainGame, self).init()

    def init_game(self):
        self.score = 0
        self.arrow.change()
        self.time_limit = 2 * MainGame.SECOND
        self.time_decrease = 40
        self.is_started = False
        self.is_game_over = False

    def update(self):
        if self.is_started and not self.is_game_over:
            if self.is_over_time():
                self.game_over()
        self.check_key()

    def is_over_time(self):
        if self.get_time() - self.time > self.time_limit:
            return True
        return False

    def get_time(self):
        return pygame.time.get_ticks()

    def check_key(self):
        for event in pygame.event.get():
            if event.type == KEYUP:
                self.check_key_exit(event)
                if not self.is_game_over:
                    self.check_key_direction(event)
                else:
                    self.check_key_reset(event)

    def check_key_exit(self, event):
        if event.key == pygame.K_ESCAPE:
            self.terminate()

    def check_key_direction(self, event):
        if event.key == pygame.K_h:
            self.check_direction('left')
        elif event.key == pygame.K_j:
            self.check_direction('up')
        elif event.key == pygame.K_k:
            self.check_direction('down')
        elif event.key == pygame.K_l:
            self.check_direction('right')

    def check_direction(self, direction):
        if not self.is_started:
            self.is_started = True
        if self.arrow.get_direction() is direction:
                self.correct_key()
        else:
            self.game_over()

    def check_key_reset(self, event):
        if event.key == pygame.K_SPACE:
            self.reset_game()

    def correct_key(self):
        self.time_limit -= self.time_decrease
        self.set_time()
        self.arrow.change()
        self.score += 1

    def set_time(self):
        self.time = pygame.time.get_ticks()

    def game_over(self):
        self.is_game_over = True
        
    def reset_game(self):
        self.init_game()

    def render_instruction(self):
        self.instruction1 = self.font.render("h : left", 0, MainGame.WHITE)
        self.instruction2 = self.font.render("j : up", 0, MainGame.WHITE)
        self.instruction3 = self.font.render("k : down", 0, MainGame.WHITE)
        self.instruction4 = self.font.render("l : right", 0, MainGame.WHITE)
        self.instruction5 = self.font.render("Spacebar : Restart ", 0, MainGame.WHITE)
        self.instruction6 = self.font.render("ESC : Exit", 0, MainGame.WHITE)
        
    def render_score(self):
        self.score_image = self.font.render("Score = %d" % self.score, 0, MainGame.WHITE)
        self.set_score_position()

    def set_score_position(self):
        self.score_pos_x = (self.window_size[0] / 2) - (self.score_image.get_width() / 2)
        if not self.is_game_over:
            self.score_pos_y = (self.window_size[1] / 10) - (self.score_image.get_height() / 2)
        else:
            self.score_pos_y = (self.window_size[1] / 2) - (self.score_image.get_height() / 2)

    def render(self, surface):
        self.render_score()
        self.render_instruction()
        surface.blit(self.score_image, (self.score_pos_x, self.score_pos_y))
        surface.blit(self.instruction1, (20, self.window_size[1] - 120))
        surface.blit(self.instruction2, (20, self.window_size[1] - 100))
        surface.blit(self.instruction3, (20, self.window_size[1] - 80))
        surface.blit(self.instruction4, (20, self.window_size[1] - 60))
        surface.blit(self.instruction5, (20, self.window_size[1] - 40))
        surface.blit(self.instruction6, (20, self.window_size[1] - 20))
        if not self.is_game_over:
            self.arrow.render(surface)

def main():
    game = MainGame()
    game.run()

if __name__ == '__main__':
    main()
