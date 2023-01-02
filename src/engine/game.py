from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python
# Imports obligatoires (dépendances, ect...)
import pygame # affichage

# Imports des autres fichiers customs
from engine.map_manager import MapManager # La gestion de la map
from display.camera_view import CameraView # la gestion de la caméra
from engine.player import Player # la gestion du joueur
from display.ingame_menu import Ingame_menu, Battle_ui # la gestion du GUI
from gameplay.battle import Battle_manager # la gestion des combats
from gameplay.equipment import Equipment # la gestion de l'equipement
from gameplay.stats import Stats # La gestion des stats + argent + level ect...

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
        map_properties = self.map_manager.get_map("map").properties
        self.player.pos = pygame.Vector2(map_properties["X_spawn_coord"], map_properties["Y_spawn_coord"])

        # on teleporte la caméra au joueur pour ne pas avoir un effet de slide au démarrage
        self.camera_view.move(1, self.player.pos, False)

        # On charge l'équipement du joueur
        self.equipment = Equipment()
        self.equipment.load() # on charge depuis le fichier de sauvegarde
        self.equipment.money = 0
        #print(self.equipment)

        # On charge le système de stats
        self.stats = Stats(self.equipment)
        
        # On initialise le menu
        self.ui = Ingame_menu(self.window,self.equipment,self.stats)
        #self.battle_ui = Battle_ui(self.ui)

        # On instancie et initialise le gestionnaire de combat (important)
        self.battle_manager = Battle_manager(self.equipment)

        # L'horloge permet à pygame de limiter la framerate du jeu, c'est purement graphique
        # on s'en sert aussi pour récupérer l'intervalle de temps (dt) entre deux frames,
        # cela permet de faire des déplacements en fonction du temps.
        self.clock = pygame.time.Clock()
        
    def run(self) -> None:
        # variable permettant de faire fonctionner la boucle de jeu.
        running = True
        restart = True
        # Initialisation des variables...
        dt = self.clock.tick(60) / 1000
        while running:
            for event in pygame.event.get():
                # pour fermer avec la croix
                if event.type == pygame.QUIT:
                    # on met la condition d'arrêt à "vrai"
                    running = False
                    restart = False
                # On envoie les evenements au joueur.
                if not self.ui.get_grab():
                    self.player.event_handler(event)
                else:
                    self.player.reset_events()
                self.ui.event_handler(event)
            
            # On récupère l'ancienne position du joueur.
            old_player_pos = self.player.pos.copy()
            # On met a jour la poisition du joueur (suivant les evenements effectués plus haut)
            self.player.move(self.map_manager, dt)
            # On récupère sa nouvelle position après déplacement
            new_player_pos = self.player.pos.copy()
            # On calcul le déplacement relatif du joueur 
            player_relative_movement = (new_player_pos - old_player_pos).magnitude()
            # On met a jour le gestionnaire de combat
            self.battle_manager.handle_player_movement(player_relative_movement)
            restart = self.battle_manager.handle_battle(self.player.pos, self.map_manager, self.stats)
            if restart:
                running = False

            # On déplace la caméra sur le joueur
            self.camera_view.move(dt, self.player.pos, False)

            # On affiche la "vue" de la caméra
            self.camera_view.draw(self.window, self.player)

            # On met a jour le compteur de fps
            self.ui.update(fps=self.clock.get_fps())
            # On met a jour la barre de combat
            if self.player.direction.magnitude() != 0:
                self.ui.update(distance=self.battle_manager.battle_chance/self.battle_manager.max_battle_chance)
            # On met a jour le compteur de combat
            self.ui.update(battle_count=(self.battle_manager.remaining_battle, self.battle_manager.number_of_battles))
            self.ui.update(stats=self.stats)
            
            self.ui.update()
            self.ui.draw()
        
            # On récupère le dt de la frame (temps entre deux frames)
            # Cet variable permet de calculer tout déplacement et evenement suivant le temps et non suivant la vitesse du jeu
            dt = self.clock.tick(60) / 1000

            # On affiche les FPS dans la console
            # (on utilise sys.stdout car le print de python est très mal optimisé et est trop gourmand pour tourner dans une boucle)
            #sys.stdout.write(str(1/dt)+"\n")

            # On met à jour l'image à l'écran suivant tout ce qu'on à calculé depuis la dernière frame.
            pygame.display.update()
        self.equipment.save()
        return restart