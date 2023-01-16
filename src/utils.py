from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python
from pathlib import Path
import pygame
import math
import pytmx

class Hitbox:
    def __init__(self, x: float, y: float, width: float, height: float):
        """
        classe pour permettre de faire des collisions comme avec les rect de pygame, mais avec des virgules.
        """

        # déffinition des attributs
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
    
    def get_pygame_rect(self):
        """
        retourne un objet pygame.Rect. Attention, cette classe ne supporte que les nb entiers
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collide(self, hitbox: Hitbox) -> bool:
        if self.x + self.width <= hitbox.x or hitbox.x + hitbox.width <= self.x :
            return False
        if self.y + self.height <= hitbox.y  or hitbox.y + hitbox.height <= self.y :
            return False
        return True

    def __str__(self):
        return f"<{self.__class__.__name__} ({self.x}, {self.y}, {self.width}, {self.height})>"

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_pygame_rect(rect: pygame.Rect) -> Hitbox:
        """
        Permet de convertir un objet pygame.Rect en objet Hitbox
        """
        return Hitbox(rect.x, rect.y, rect.width, rect.height)

class DynamicImage:
    """
    Une classe qui permet à une image de s'occuper individuellement de sa propre taille / niveau de zoom.
    """
    def __init__(self, image: pygame.Surface, smooth: bool=False) -> None:
        self._original_image = image
        self._resized_image = image
        self._current_factor = 1

        self._original_image_width = self._original_image.get_width()
        self._original_image_height = self._original_image.get_height()

        self._smooth = smooth

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
            return DynamicImage(tile_surface, smooth=False)
        return extract_image


def number_to_str(nb:int|float)->str:
    """
    Permet de transformer un entier en string en rajoutant du formatage
    par exemple : 1000 -> 1k
    """
    def only_three_digits(number):
        """
        retourne en nombre contenant trois chiffres au maximum
        """
        if number >= 100:
            return round(number)
        if number >= 10:
            return int(number*10)/10
        return int(number*100)/100

    # On définit les unités
    unities = ["","k","m","b","t","q"]
    for unity in unities:
        if nb < 1000:
            return str(only_three_digits(nb))+unity
        nb = nb/1000
    
    return str(only_three_digits(nb))+"Q"