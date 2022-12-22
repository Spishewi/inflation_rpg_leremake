from __future__ import annotations
import pytmx
import pygame
import math
from pathlib import Path
import numpy as np
from utils import DynamicImage

class MapManager:
    def __init__(self) -> None:
        self._maps: dict[pytmx.TiledMap]= {}

    def add_map(self, map_name: str, map_path: Path) -> None:
        """
        Permet d'ajouter une map au gestionnaire
        """
        # On vérifie que aucune map s'appelle comme ça
        if map_name in self._maps.keys():
            raise ValueError(f"{map_name} is already used")

        # On crée la map
        new_map = pytmx.TiledMap(map_path, image_loader=DynamicImage.image_loader)

        # On l'ajoute à la liste de maps
        self._maps[map_name] = new_map
    
    def get_map(self, map_name: str) -> pytmx.TiledMap:
        return self._maps[map_name]

    def get_around_collisions(self, map_name: str, coords: pygame.Vector2, size: int, layers_names: list):
        map = self.get_map(map_name)

        minx = max(0, math.floor(coords.x) - size)
        maxx = min(map.width, math.ceil(coords.x) + size)
        miny = max(0, math.floor(coords.y) - size)
        maxy = min(map.height, math.ceil(coords.y) + size)
        
        # pareil les discitonnaires sont pas opti comme structure, faudrait trouver autre chose
        around_collisions = {}
        for layer_name in layers_names:
            layer = map.get_layer_by_name(layer_name)
            
            # append est gourmande comme fonction, donc j'ai écrit comme ça, ça devrait être plus opti
            # ça fait la même chose
            # techiniquement je pourrais même utiliser les dictionnaires en comprehension, mais pour deux/3 tours de boucle,
            # on perdrais en lisibilité pour pas grand chose
            #print(layer.data)
            tiles = [(x, y) for x in range(minx, maxx) for y in range(miny, maxy) if layer.data[y][x] != 0]
            # voici le code sans liste en compréhension
            """
            for x in range(minx, maxx):
                for y in range(miny, maxy):
                    if layer.data[x][y] != 0:
                        tiles.append((x, y))"""
            around_collisions[layer_name] = tiles
        return around_collisions
    
    def get_level_range(self, map_name: str, coords: pygame.Vector2) -> range:
        # on veux savoir les coordonnées de la tile sur laquelle est le joueur.
        coords.x = round(coords.x)
        coords.y = round(coords.y)

        # on vérifie si on est dans la map (on sais jamais ce qui peut arriver)
        map = self.get_map(map_name)
        if not (0 <= coords.x <= map.width and 0 <= coords.y <= map.height):
            return

        # on récupère le layer des zones
        layer = map.get_layer_by_name("levels zones")
        # on récupère les propriété de la tile où se trouve le joueur
        tile_properties = map.get_tile_properties(coords.x, coords.y, layer)
        # on lit le niveau de la zone
        tile_level = tile_properties["level"]

        # on retourne l'intervalle de niveau correspondant
        return range(tile_level*10, (tile_level+1)*10)

