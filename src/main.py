import pygame

from engine.game import Game
from engine.title_screen import Title_screen

pygame.init()

if __name__ == '__main__':
    window = pygame.display.set_mode((1200, 650))
    title_screen = Title_screen(window)
    #title_screen_launch_game = title_screen.run()
    title_screen_launch_game = True
    if title_screen_launch_game:
        game = Game(window)
        game.run()
