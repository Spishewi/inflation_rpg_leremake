from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python

import pygame
pygame.init()

from engine.game import Game
from engine.title_screen import Title_screen

"""
Comme vous l'avez demandé, on à rétréci ce fichier au maximum.
Tout le reste à part ce fichier est exclusivement de la POO.
"""


# Se lance quand on lance le fichier
if __name__ == '__main__':

    # On crée la fenêtre
    window = pygame.display.set_mode((1200, 650))

    # On donne un titre à la fenêtre
    pygame.display.set_caption("Inflation RPG Leremake")

    # On crée la boucle principale
    running = True
    game_launch_title_screen = True
    first_game = True

    while running:
        # On lance le titlescreen
        if game_launch_title_screen:
            title_screen = Title_screen(window,first_game)
            """
            Cette fonction retourne Vrai ou Faux suivant si l'utilisateur veux lancer le jeu.
            """
            title_screen_launch_game = title_screen.run()
        else:
            running = False
        first_game = False
        
        # On lance le jeu
        if title_screen_launch_game and running:
            game = Game(window)
            game_launch_title_screen = game.run()
            print("FIN DU JEU")
        else:
            running = False
