import pygame

from engine.game import Game

pygame.init()

if __name__ == '__main__':
    window = pygame.display.set_mode((1200, 650))
    game = Game(window)
    game.run()
