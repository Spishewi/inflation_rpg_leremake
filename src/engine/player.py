from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python
import pygame
import math
from utils import Hitbox
from display.graphics import Animation

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 10
        self.hitbox_decalage = 0.6
        self.animation  = Animation("../graphics/player_keyframes")
    
    def get_animation(self, factor): # Renvoie l'annimation du joueur en fonction de sa direction
        return self.animation.get_curentAnimation(self.direction, factor)

    def get_rect(self): # Revoie le rectangle dans lequel le joueur sera affiché 
        return pygame.Rect(self.pos.x, self.pos.y, 1, 1)

    def get_hitbox(self): # Renvoie la hitbox du joueur
        return Hitbox(self.pos.x, self.pos.y+self.hitbox_decalage, 1, 0.5)

    def move(self, map_manager, dt: float):
        if self.direction.magnitude() != 0:
            # On récupère les tuiles aux alentours du joueur qui doivent avoir une collision
            collisions_tiles = map_manager.get_around_collisions("map",self.pos, 2, ["collisions"])["collisions"]
            velocity = self.direction.normalize() * self.speed * dt
            
            step = max(math.ceil(abs(velocity.y)), math.ceil(abs(velocity.x)))
            for i in range(step):
                # On fait avancer le joueur en x
                self.pos.x += velocity.x / step
                # On corrige son x si il y a une collision
                self.collisions("x", velocity, collisions_tiles)
                # On fait avancer le joueur en y
                self.pos.y += velocity.y / step
                # On corrige son y si il y a une collision
                self.collisions("y", velocity, collisions_tiles)
                
    def collisions(self, direction: str, velocity: float, collisions: list) -> pygame.Vector2:
        """
            Change la position du joueur si il y a une colision
            collision : liste des tiles susceptibles d'être en collision avec le joueur
        """
        player_hitbox = self.get_hitbox()
        for tile_pos in collisions: # On regarde pour toutes les tuiles aux alentours du joueur qui doivent avoir une collision
            # On récupère la hitbox de la tuile
            tile_hitbox = Hitbox(tile_pos[0], tile_pos[1], 1, 1)
            
            if tile_hitbox.overlap2(player_hitbox): # Si il y a une collision
                
                if direction == "y":
                    if velocity.y > 0: # Moving down
                        self.pos.y = tile_hitbox.y - player_hitbox.height - self.hitbox_decalage
                    elif velocity.y < 0: # Moving up
                        self.pos.y = tile_hitbox.y + tile_hitbox.height - self.hitbox_decalage
                        
                elif direction == "x":   
                    if velocity.x > 0: # Moving right
                        self.pos.x = tile_hitbox.x - player_hitbox.width

                    elif velocity.x < 0: # Moving left
                        self.pos.x = tile_hitbox.x + player_hitbox.width

                # On récupère la nouvelle hitbox du joueur
                player_hitbox = self.get_hitbox()

    def event_handler(self, event: pygame.event): 
        """
            définit la direction du joueur en fonction des touches pressées
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
        
        # Pour corriger des pb quand des inputs sont sauté,
        # on réinitialise au cas où les inputs quand on touche pas au clavier
        key_sequence = pygame.key.get_pressed()
        if (not key_sequence[pygame.K_LEFT] and
            not key_sequence[pygame.K_RIGHT] and
            not key_sequence[pygame.K_UP] and
            not key_sequence[pygame.K_DOWN] and
            not key_sequence[pygame.K_z] and
            not key_sequence[pygame.K_q] and 
            not key_sequence[pygame.K_s] and
            not key_sequence[pygame.K_d]):
            self.reset_events()


    def reset_events(self):
        self.direction.x = 0
        self.direction.y = 0