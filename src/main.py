from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python

import pygame

from engine.game import Game
from engine.title_screen import Title_screen

pygame.init()

if __name__ == '__main__':
    window = pygame.display.set_mode((1200, 650))
    running = True
    game_launch_title_screen = True
    while running:
        if game_launch_title_screen:
            title_screen = Title_screen(window)
            title_screen_launch_game = title_screen.run()
        else:
            running = False
            
        if title_screen_launch_game and running:
            game = Game(window)
            game_launch_title_screen = game.run()
            print("FIN DU JEU")
        else:
            running = False
