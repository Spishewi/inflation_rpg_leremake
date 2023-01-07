from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python
# Imports obligatoires (dépendances, ect...)
import pygame # affichage

# Imports des autres fichiers customs
from engine.map_manager import MapManager # La gestion de la map
from display.camera_view import CameraView # la gestion de la caméra
from engine.player import Player # la gestion du joueur
from display.ingame_menu import Ingame_menu, Battle_ui, End_menu # la gestion du GUI
from gameplay.battle import Battle_manager # la gestion des combats
from gameplay.equipment import Equipment # la gestion de l'equipement
from gameplay.stats import Stats # La gestion des stats + argent + level ect...
from utils import Hitbox # les hitbox pour detecter la zone de fin

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
        spawn_point = self.map_manager.get_map("map").get_object_by_name("spawnpoint_leftcorner")
        self.player.pos = pygame.Vector2(spawn_point.x/16,spawn_point.y/16)

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
        self.ui = Ingame_menu(self.window,self)
        self.battle_ui = Battle_ui(self.ui)
        self.end_menu = End_menu(self.ui)
        self.ui_grab_state = False

        # On instancie et initialise le gestionnaire de combat (important)
        self.battle_manager = Battle_manager(self.battle_ui)
        
        exit_rect = self.map_manager.get_map("map").get_object_by_name("final_boss_and_end_gate")
        self.exit_rect = Hitbox(exit_rect.x/16,exit_rect.y/16,exit_rect.width/16,exit_rect.height/16)
        
        self.restart = False

        # L'horloge permet à pygame de limiter la framerate du jeu, c'est purement graphique
        # on s'en sert aussi pour récupérer l'intervalle de temps (dt) entre deux frames,
        # cela permet de faire des déplacements en fonction du temps.
        self.clock = pygame.time.Clock()
        
    def run(self) -> None:
        # Initialisation des variables permettant de faire fonctionner la boucle de jeu.
        running = True          # Si =True alors le jeu tourne
        
        self.restart = False    # Quand une des deux est égale à True alors le jeu
        restart = False         # s'arrète et l'écran de titre est ouvert
        
        last_battle = False     # Indique si la bataille contre le boss final est en cours
       
        # On récupère le dt de la frame (temps entre deux frames)
        # Cette variable permet de calculer tout déplacement et évènement suivant le temps et non suivant la vitesse du jeu
        dt = self.clock.tick(60) / 1000
        
        # Boucle de jeu :
        while running:
            # On regarde les evenements pygame (entrées clavier et clicks souris)
            # et on met à jour tous les éléments qui y sont liés
            for event in pygame.event.get():
                # Pour fermer avec la croix
                if event.type == pygame.QUIT:
                    # On met la condition d'arrêt à "vrai"
                    running = False
                    restart = False
                # On envoie les evenements au joueur
                # seulement si aucun menu n'est ouvert
                if self.ui.get_grab() != self.ui_grab_state:
                    # On reset à l'ouverture et à la fermeture des menus pour éviter des bugs
                    self.player.reset_events()
                    self.ui_grab_state = self.ui.get_grab()
                    
                if not self.ui_grab_state:
                    self.player.event_handler(event)
                else :
                    self.player.reset_events()
                # On envoie les events à l'interface
                self.ui.event_handler(event)
            
            # On récupère l'ancienne position du joueur.
            old_player_pos = self.player.pos.copy()
            if not self.ui.get_grab():
                # On met a jour la poisition du joueur (suivant les évènements effectués plus haut)
                self.player.move(self.map_manager, dt)
            # On récupère sa nouvelle position après déplacement
            new_player_pos = self.player.pos.copy()
            # On calcul le déplacement relatif du joueur 
            player_relative_movement = (new_player_pos - old_player_pos).magnitude()
            # On met a jour le gestionnaire de combat
            self.battle_manager.handle_player_movement(player_relative_movement)
            restart = self.battle_manager.handle_battle(self.player.pos, self.map_manager, self.stats)
            # Si la partie est finie et que le menu de combat n'est pas ouvert
            # ou si le bouton title screen est cliqué (self.restart)
            if (restart and not self.battle_ui.battle_ui_opened) or self.restart:
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
            # On met a jour l'affichage du niveau
            self.ui.update(level=self.stats.lvl)
            self.ui.update(stats=self.stats.get_player_entity())
            
            # On met à jour les widget en général
            self.ui.update()
            # Si l'affichage de combat est ouvert, on affiche une nouvelle ligne,
            # la fonction se charge elle même de l'intervalle de temps entre ces affichages
            self.battle_ui.update()
            # On affiche tous les widgets et toutes les modifications faites précédemment
            self.ui.draw()

            # On lance le combat de boss/final si le joueur est situé près de la sortie
            if self.exit_rect.overlap2(self.player.get_hitbox()) and not last_battle:
                self.battle_manager.must_trigger_battle = True
                last_battle = True
                # On écarte le joueur de la porte pour éviter de relancer un combat instantanément si il perd
                self.player.pos.y = self.player.pos.y +2

            # Si le combat final à été lancé
            if last_battle:
                # Si le joueur a gagné et qu'il a fermé l'interface de combat
                if self.battle_manager.round_result == "win" and not self.battle_ui.battle_ui_opened:
                    print("YOU WIN")
                    # On affiche la page de fin
                    self.end_menu.start()
                    
                # Si le joueur a perdu
                elif self.battle_manager.round_result == "lost":
                    last_battle = False # combat n'est plus en cours et le jeu reprend

        
            # On récupère le dt de la frame (temps entre deux frames)
            dt = self.clock.tick(60) / 1000

            # On affiche les FPS dans la console
            # (on utilise sys.stdout car le print de python est très mal optimisé et est trop gourmand pour tourner dans une boucle)
            # sys.stdout.write(str(1/dt)+"\n")

            # On met à jour l'image à l'écran suivant tout ce qu'on à calculé depuis la dernière frame.
            pygame.display.update()
        self.equipment.save()
        return self.restart or restart