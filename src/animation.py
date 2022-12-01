from __future__ import annotations
from utils import DynamicImage
import pygame
import json


class Animation:
    def __init__(self, path: str):
        self.previousDirection = pygame.Vector2(0,0)
        spritesheet = pygame.image.load(f"{path}/image.png")
        spritesheet = spritesheet.convert_alpha()
        with open(f"{path}/keyframes.json") as animation_settings:
            self.SETTINGS = json.load(animation_settings)

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
        self.direction = direction
        speed = 150
        ticks = int(pygame.time.get_ticks()/speed)%2

        if self.direction.x == 0 and self.direction.y == 0 : # immobile
            if self.previousDirection.x == 0 and self.previousDirection.y == 0:
                direction_name = "down"
            elif self.previousDirection.x == 1 and self.previousDirection.y == 0 : # droite
                direction_name = "right"
            elif self.previousDirection.x == 1 and self.previousDirection.y == 1 : # diagonale bas droite
                direction_name = "down-right"
            elif self.previousDirection.x == 0 and self.previousDirection.y == 1 : # bas
                direction_name = "down"
            elif self.previousDirection.x == -1 and self.previousDirection.y == 1 : # diagonale bas gauche
                direction_name = "down-left"
            elif self.previousDirection.x == -1 and self.previousDirection.y == 0 : # gauche
                direction_name = "left"
            elif self.previousDirection.x == -1 and self.previousDirection.y == -1 : # diagonale haut gauche
                direction_name = "up-left"
            elif self.previousDirection.x == 0 and self.previousDirection.y == -1 : # haut
                direction_name = "up"
            elif self.previousDirection.x == 1 and self.previousDirection.y == -1 : # diagonale haut droit
                direction_name = "up-right"

            self.previousDirection = pygame.Vector2(self.previousDirection.x,self.previousDirection.y)
            return self.sprites[direction_name]["idle"].get_image(factor)

        elif self.direction.x == 1 and self.direction.y == 0 : # droite
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["right"]["frames"][ticks].get_image(factor)
        elif self.direction.x == 1 and self.direction.y == 1 : # diagonale bas droite
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["down-right"]["frames"][ticks].get_image(factor)
        elif self.direction.x == 0 and self.direction.y == 1 : # bas
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["down"]["frames"][ticks].get_image(factor)
        elif self.direction.x == -1 and self.direction.y == 1 : # diagonale bas gauche
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["down-left"]["frames"][ticks].get_image(factor)
        elif self.direction.x == -1 and self.direction.y == 0 : # gauche
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["left"]["frames"][ticks].get_image(factor)
        elif self.direction.x == -1 and self.direction.y == -1 : # diagonale haut gauche
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["up-left"]["frames"][ticks].get_image(factor)
        elif self.direction.x == 0 and self.direction.y == -1 : # haut
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["up"]["frames"][ticks].get_image(factor)
        elif self.direction.x == 1 and self.direction.y == -1 : # diagonale haut droit
            self.previousDirection = pygame.Vector2(self.direction.x,self.direction.y)
            return self.sprites["up-right"]["frames"][ticks].get_image(factor)