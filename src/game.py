from map_manager import MapManager
from camera_view import CameraView
from player import Player
import pygame
import math
import sys

class Game:
    def __init__(self, window):
        self.window = window

        self.map_manager = MapManager()
        self.map_manager.add_map("map", "../graphics/map.tmx")
        print("map added")

        self.camera_view = CameraView(self.map_manager, 3)
        self.camera_view.set_map("map")
        self.camera_view.set_zoom(1)
        print("camera loaded and connected")

        self.player = Player()
        self.player.pos = pygame.Vector2(40, 40)

        self.clock = pygame.time.Clock()
        
    def run(self):
        running = True
        dt = 1
        while running:
            for event in pygame.event.get():
                # pour fermer avec la croix
                if event.type == pygame.QUIT:
                    # on met la condition d'arret a vraie
                    running = False
                self.player.event_handler(event)
            
            #coords = pygame.Vector2(math.cos(pygame.time.get_ticks()/1000 / 2)*10+40, math.sin(pygame.time.get_ticks()/1000)*10+40)
            self.player.move(self.map_manager, dt)
            self.camera_view.move(dt, self.player.pos, True)
            self.camera_view.draw(self.window, self.player)
        
            dt = self.clock.tick(60) / 1000
            pygame.display.update()