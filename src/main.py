import pygame

from game import Game

pygame.init()

if __name__ == '__main__':
    window = pygame.display.set_mode((1440, 720))
    game = Game(window)
    game.run()
