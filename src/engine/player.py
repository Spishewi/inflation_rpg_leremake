from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python
import pygame
import math
from utils import Hitbox, DynamicImage
from display.graphics import Animation

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 10
        #self.image = DynamicImage(pygame.image.load("../graphics/player.png"))
        self.hitbox_decalage = 0.6
        self.animation  = Animation("../graphics/player_keyframes")
    
    def get_animation(self, factor):
        return self.animation.get_curentAnimation(self.direction, factor)

    def get_rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, 1, 1)

    def get_hitbox(self):
        return Hitbox(self.pos.x, self.pos.y+self.hitbox_decalage, 1, 0.5)

    def move(self, map_manager, dt: float):
        if self.direction.magnitude() != 0:
            collisions_tiles = map_manager.get_around_collisions("map",self.pos, 2, ["collisions"])["collisions"]
            #print(self.pos, collisions_tiles)
            velocity = self.direction.normalize() * self.speed * dt
            #self.pos += velocity
            
            step = max(math.ceil(abs(velocity.y)), math.ceil(abs(velocity.x)))
            for i in range(step):
                self.pos.x += velocity.x / step
                self.collisions("x", velocity, collisions_tiles)
                self.pos.y += velocity.y / step
                self.collisions("y", velocity, collisions_tiles)
                
    def collisions(self, direction: str, velocity: float, collisions: list) -> pygame.Vector2:
        """
            Change la position du joueur si il y a une colision
            collision : liste des tiles susceptibles d'être en collision avec le joueur
        """
        player_hitbox = self.get_hitbox()
        for tile_pos in collisions:
            tile_hitbox = Hitbox(tile_pos[0], tile_pos[1], 1, 1)
            
            if tile_hitbox.overlap2(player_hitbox): # si il y a une collision
                #print("collisions", tile_rect)
                
                if direction == "y":
                    if velocity.y > 0: # moving down
                        self.pos.y = tile_hitbox.y - player_hitbox.height - self.hitbox_decalage
                    elif velocity.y < 0: # moving up
                        self.pos.y = tile_hitbox.y + tile_hitbox.height - self.hitbox_decalage
                        
                elif direction == "x":   
                    if velocity.x > 0: # moving right
                        self.pos.x = tile_hitbox.x - player_hitbox.width

                    elif velocity.x < 0: # moving left
                        self.pos.x = tile_hitbox.x + player_hitbox.width

                player_hitbox = self.get_hitbox()

    def event_handler(self, event: pygame.event): 
        """
            defini la direction du joueur en fonction des touches pressés
        """        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                self.direction.x -= 1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.direction.x += 1
            elif event.key == pygame.K_UP or event.key == pygame.K_z:
                self.direction.y -= 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.direction.y += 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                self.direction.x += 1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.direction.x -= 1
            elif event.key == pygame.K_UP or event.key == pygame.K_z:
                self.direction.y += 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.direction.y -= 1

    def reset_events(self):
        self.direction.x = 0
        self.direction.y = 0