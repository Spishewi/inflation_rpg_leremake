from __future__ import annotations
from utils import DynamicImage
import pygame
import json



class Animation():
    def __init__(self, path: str):

        # On charge la feuille de sprite
        spritesheet = pygame.image.load(f"{path}/image.png")
        self.spritesheet = spritesheet.convert_alpha()
        with open(f"{path}/keyframes.json") as animation_settings:
            self.SETTINGS = json.load(animation_settings)

        # On definit le reste des attributs
        self.previousDirection = [0,0]
        self.sprites = self.load_sprites(self.spritesheet)
        
    def load_sprites(self, spritesheet):
        """
        Charge les annimations dans un dict en fonction de 'keyframes.json'
        et les tris de manière à ce que l'on puisse y accéder facilement.
        """
        sprites = {}

        for k,v in self.SETTINGS["keyframes"].items():
            sprites[k] = {}
            sprites[k]["frames"] = []
            for x in range(v["frames"][0][0], v["frames"][1][0]+1):
                for y in range(v["frames"][0][1], v["frames"][1][1]+1):
                    rect = (x * self.SETTINGS["sprite_width"], y * self.SETTINGS["sprite_width"], self.SETTINGS["sprite_width"], self.SETTINGS["sprite_height"])
                    tile_surface = pygame.Surface((self.SETTINGS["sprite_width"], self.SETTINGS["sprite_height"]), pygame.SRCALPHA)
                    tile_surface.blit(spritesheet, (0, 0), rect)
                    if v["flip"]:
                        tile_surface = pygame.transform.flip(tile_surface, True, False)
                    sprites[k]["frames"].append(DynamicImage(tile_surface))

            rect = (v["idle"][0] * self.SETTINGS["sprite_width"], v["idle"][1] * self.SETTINGS["sprite_width"], self.SETTINGS["sprite_width"], self.SETTINGS["sprite_height"])
            tile_surface = pygame.Surface((self.SETTINGS["sprite_width"], self.SETTINGS["sprite_height"]), pygame.SRCALPHA)
            tile_surface.blit(spritesheet, (0, 0), rect)
            if v["flip"]:
                tile_surface = pygame.transform.flip(tile_surface, True, False)
            sprites[k]["idle"] = DynamicImage(tile_surface)
            
        return sprites
    
    def get_curentAnimation(self, direction: pygame.Vector2, factor) -> DynamicImage:
        """
        renvoie la frame (une DynamicImage) correspondante à l'instant T pour l'animation en fonction de la direction du joueur
        """
        direction = direction.xy
        speed = 150
        ticks = int(pygame.time.get_ticks()/speed)%2 # nombre entre 1 et 2 pour le numero de l'annimation à selectionner (ici il n'y en a que deux de possibles)
        
        for i in range(2): # permet d'éviter que le x ou le y soit à 2 pour les conditions d'après
            if direction[i] > 1:
                direction[i] = 1
            elif direction[i] < -1:
                direction[i] = -1
        
        if direction == [0,0] : # immobile -> il reste dans la direction de sa précédente action
            if self.previousDirection == [0,0]:
                return self.sprites["down"]["idle"].get_image(factor)
            elif self.previousDirection == [1,0] : # droite
                return self.sprites["right"]["idle"].get_image(factor)
            elif self.previousDirection == [1,1] : # diagonale bas droite
                return self.sprites["down-right"]["idle"].get_image(factor)
            elif self.previousDirection == [0,1] : # bas
                return self.sprites["down"]["idle"].get_image(factor)
            elif self.previousDirection == [-1,1] : # diagonale bas gauche
                return self.sprites["down-left"]["idle"].get_image(factor)
            elif self.previousDirection == [-1,0] : # gauche
                return self.sprites["left"]["idle"].get_image(factor)
            elif self.previousDirection == [-1,-1] : # diagonale haut gauche
                return self.sprites["up-left"]["idle"].get_image(factor)
            elif self.previousDirection == [0,-1] : # haut
                return self.sprites["up"]["idle"].get_image(factor)
            elif self.previousDirection == [1,-1] : # diagonale haut droit
                return self.sprites["up-right"]["idle"].get_image(factor)
        
        elif direction == [1,0] :# droite
            self.previousDirection = direction
            return self.sprites["right"]["frames"][ticks].get_image(factor)
        elif direction == [1,1] : # diagonale bas droite
            self.previousDirection = direction
            return self.sprites["down-right"]["frames"][ticks].get_image(factor)
        elif direction == [0,1] : # bas
            self.previousDirection = direction
            return self.sprites["down"]["frames"][ticks].get_image(factor)
        elif direction == [-1,1] : # diagonale bas gauche
            self.previousDirection = direction
            return self.sprites["down-left"]["frames"][ticks].get_image(factor)
        elif direction == [-1,0] : # gauche
            self.previousDirection = direction
            return self.sprites["left"]["frames"][ticks].get_image(factor)
        elif direction == [-1,-1] : # diagonale haut gauche
            self.previousDirection = direction
            return self.sprites["up-left"]["frames"][ticks].get_image(factor)
        elif direction == [0,-1] : # haut
            self.previousDirection = direction
            return self.sprites["up"]["frames"][ticks].get_image(factor)
        elif direction == [1,-1] : # diagonale haut droit
            self.previousDirection = direction
            return self.sprites["up-right"]["frames"][ticks].get_image(factor)


class Objects_picture():
    def __init__(self, path:str) -> None:
        """
        Permet de charger plusieurs images à partir d'une feuille de sprite unique.
        """

        spritesheet = pygame.image.load(f"{path}/image.png")
        self.spritesheet = spritesheet.convert_alpha()
        with open(f"{path}/keyframes.json") as animation_settings:
            self.SETTINGS = json.load(animation_settings)
            
        self.sprites = self.load_sprites(self.spritesheet)
        
    def load_sprites(self, spritesheet):
        """
        charge les annimations dans un dict en fonction de 'keyframes.json', et les tris de façon à faciliter l'accès.
        """
        sprites = {}
        for k,v in self.SETTINGS["keyframes"].items():
            
            sprites[k] = []
            for x in range(v[0][0], v[1][0]+1):
                for y in range(v[0][1], v[1][1]+1):
                    rect = (x * self.SETTINGS["sprite_width"], y * self.SETTINGS["sprite_width"], self.SETTINGS["sprite_width"], self.SETTINGS["sprite_height"])
                    tile_surface = pygame.Surface((self.SETTINGS["sprite_width"], self.SETTINGS["sprite_height"]), pygame.SRCALPHA)
                    tile_surface.blit(spritesheet, (0, 0), rect)
                    sprites[k].append(DynamicImage(tile_surface))
            
        return sprites
    
    def get_object_picture(self, object_type:str,number:int,zoom_factor:int):
        """
            Permet d'obtenir une image pour un objet donné
        """
        return self.sprites[object_type][number].get_image(zoom_factor)