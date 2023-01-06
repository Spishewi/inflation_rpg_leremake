from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python

from display.title_screen_menu import Title_screen_menu
import pygame
from gameplay.equipment import Equipment

class Title_screen():
    def __init__(self, window: pygame.Surface, first_game:bool) -> None:
        # On charge l'équipment du joueur
        self.equipment = Equipment()
        self.equipment.load()
        
        # On initialise l'affichage
        self.ui = Title_screen_menu(window,self.equipment, first_game)

        self.clock = pygame.time.Clock()
    
    def run(self) -> bool:
        # variable permettant de faire fonctionner la boucle de jeu.
        # Initialisation des variables...
        dt = self.clock.tick(0) / 1000
        running = True
        while running:
            for event in pygame.event.get():
                # pour fermer avec la croix
                if event.type == pygame.QUIT or self.ui.must_quit:
                    # on ferme sans lancer le jeu
                    return False
                self.ui.event_handler(event)
            
            

            if self.ui.must_start:
                running = False
            
            self.ui.update()
            self.ui.draw()

            dt = self.clock.tick(0) / 1000
            
            pygame.display.update()
        self.equipment.save()
        return True