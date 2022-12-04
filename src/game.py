from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python
# Imports obligatoires (dépendances, ect...)
import pygame # affichage
import math # calculs divers
import sys # actions spéciales du système (sys.stdout.write() et sys.exit())

# Imports des autres fichiers customs
from map_manager import MapManager # La gestion de la map
from camera_view import CameraView # la gestion de la caméra
from player import Player # la gestion du joueur



class Game:
    """
    cette classe gère le jeu en lui mème, (elle correspond à une partie)
    """
    def __init__(self, window: pygame.Surface) -> None:
        # On enregistre la fenêtre où l'on va dessiner
        self.window = window

        # On initialise le map Manager
        self.map_manager = MapManager()
        self.map_manager.add_map("map", "../graphics/map2.tmx")
        print("map added")

        # On initialise la caméra
        self.camera_view = CameraView(self.map_manager, 2)
        self.camera_view.set_map("map")
        self.camera_view.set_zoom(2.5)
        print("camera loaded and connected")

        # On initialise le joueur
        self.player = Player()
        self.player.pos = pygame.Vector2(53, 48)

        # on teleporte la caméra au joueur pour pas avoir un effet de slide au démarrage
        self.camera_view.move(1, self.player.pos, False)


        self.clock = pygame.time.Clock()
        
    def run(self) -> None:
        # variable permettant de faire fonctionner la boucle de jeu.
        running = True
        # Initialisation des variables...
        dt = self.clock.tick(0) / 1000
        while running:
            for event in pygame.event.get():
                # pour fermer avec la croix
                if event.type == pygame.QUIT:
                    # on met la condition d'arrêt à "vrai"
                    running = False
                # On envoie les evenements au joueur.
                self.player.event_handler(event)
            
            # On met a jour la poisition du joueur (suivant les evenements effectués plus haut)
            self.player.move(self.map_manager, dt)

            # On déplace la caméra sur le joueur
            self.camera_view.move(dt, self.player.pos, False)

            # On affiche la "vue" de la caméra
            self.camera_view.draw(self.window, self.player)
        
            # On récupère le dt de la frame (temps entre deux frames)
            # Cet variable permet de calculer tout déplacement et evenement suivant le temps et non suivant la vitesse du jeu
            dt = self.clock.tick(0) / 1000

            # On affiche les FPS
            # (on utilise sys.stdout car le print de python est très mal optimisé et est trop gourmand pour tourner dans une boucle)
            #sys.stdout.write(str(1/dt)+"\n")

            # On met à jour l'image à l'écran suivant tout ce qu'on à calculé depuis la dernière frame.
            pygame.display.update()