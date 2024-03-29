from __future__ import annotations # Permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python

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
        # Variable permettant de faire fonctionner la boucle de jeu.
        # Initialisation des variables...
        dt = self.clock.tick(0) / 1000
        running = True
        while running:
            for event in pygame.event.get():
                # Pour fermer avec la croix
                if event.type == pygame.QUIT or self.ui.must_quit:
                    # On ferme sans lancer le jeu
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.ui.play_menu()
                self.ui.event_handler(event)
            
            
            # Si le menu l'indique la partie se termine et le menu de titre est ouvert
            if self.ui.must_start:
                running = False
            
            # Met à jour l'affichage
            self.ui.update()
            self.ui.draw()

            dt = self.clock.tick(0) / 1000
            
            pygame.display.update()
        self.equipment.save()
        return True