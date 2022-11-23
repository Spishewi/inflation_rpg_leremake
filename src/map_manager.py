import pytmx
import pygame
import math
from pathlib import Path
import numpy as np

class MapManager:
    def __init__(self) -> None:
        self._maps = {}

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
            tiles = [(x, y) for x in range(minx, maxx) for y in range(miny, maxy) if layer.data[x][y] != 0]
            """
            for x in range(minx, maxx):
                for y in range(miny, maxy):
                    if layer.data[x][y] != 0:
                        tiles.append((x, y))"""
            around_collisions[layer_name] = tiles
        return around_collisions




class DynamicImage:
    """
    Une classe qui permet à une image de s'occuper individuellement de sa propre taille / niveau de zoom.
    """
    def __init__(self, id_tile: str, image: pygame.Surface, smooth: bool=False) -> None:
        self._original_image = image
        self._resized_image = image
        self._current_factor = 1

        self._original_image_width = self._original_image.get_width()
        self._original_image_height = self._original_image.get_height()

        self._smooth = smooth
        self.id_tile = id_tile

        pixels_alpha_array = pygame.surfarray.pixels_alpha(self._original_image).flatten()

        self.opaque = True
        for pixel in pixels_alpha_array:
            if pixel == 0:
                self.opaque = False
                #pygame.draw.rect(self._original_image, (127, 255, 127), (6, 6, 4, 4))
                break
        

    def get_image(self, factor: float) -> pygame.Surface:
        """
        Permet récupérer l'image de bonne taille en fonction d'un facteur.
        L'image est si besoin redimentionné, et mise en cache.
        """
        if factor <= 0:
            raise ValueError("factor must be > 0")

        if factor != self._current_factor:
            self._current_factor = factor
            new_size = (math.floor(self._original_image_width*factor), math.floor(self._original_image_height*factor))
            if self._smooth:
                self._resized_image = pygame.transform.smoothscale(self._original_image, size=new_size)
            else:
                self._resized_image = pygame.transform.scale(self._original_image, size=new_size)
            #self._resized_image = self._resized_image.convert_alpha()
        return self._resized_image

    @staticmethod
    def image_loader(file_path: Path, colorkey=None, **kwargs):
        """
        pytmx.TiledMap() utilise cette fonction pour charger toutes ses images.
        """

        tileset_image = pygame.image.load(file_path)
        tileset_image = tileset_image.convert_alpha()
        tileset_image.set_colorkey(colorkey)

        def extract_image(rect: tuple, flags: pytmx.TileFlags) -> DynamicImage:
            tile_size = rect[2]
            tile_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            tile_surface.blit(tileset_image, (0, 0), rect)
            #tile_surface = tile_surface.convert_alpha()
            return DynamicImage(file_path + str(rect), tile_surface, smooth=False)
        return extract_image

if __name__ == "__main__":
    map_manager = MapManager()
    map_manager.add_map("level_0", "../graphics/map/level_0/map3.tmx")