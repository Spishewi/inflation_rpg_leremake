from __future__ import annotations
from utils import DynamicImage
import pygame
import json


class Animation:
    def __init__(self, path: str):
        self.previousDirection = [0,0]
        spritesheet = pygame.image.load(f"{path}/image.png")
        spritesheet = spritesheet.convert_alpha()
        with open(f"{path}/keyframes.json") as animation_settings:
            self.SETTINGS = json.load(animation_settings)
            
        '''
        self.animations = {
            "00":"down",
            "10":"right",
            "11":"down-right",
            "01":"down",
            "-11":"down-left",
            "-10":"left",
            "-1-1":"up-left",
            "0-1":"up",
            "1-1":"up-right"
        }'''

        self.sprites = self.load_sprites(spritesheet)
        
    def load_sprites(self, spritesheet):
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
        direction = direction.xy
        speed = 150
        ticks = int(pygame.time.get_ticks()/speed)%2
        
        for i in range(2):
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
        
        '''
        if direction == [0,0] :
            return self.sprites[self.animations[str(int(self.previousDirection[0]))+str(int(self.previousDirection[1]))]]["idle"].get_image(factor)
        else:
            self.previousDirection = direction
            return self.sprites[self.animations[str(int(direction[0]))+str(int(direction[1]))]]["frames"][ticks].get_image(factor)
        '''