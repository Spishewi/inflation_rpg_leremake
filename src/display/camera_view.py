from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python
# Imports obligatoires (dépendances, ect...)
import pygame # affichage
import math # calculs divers

# Imports des autres fichiers customs
from engine.map_manager import MapManager # La gestion de la map

class CameraView:
    """
    permet d'afficher une partie d'une map
    """
    def __init__(self, map_manager: MapManager, move_ease: float) -> None:

        # création des variables utiles
        self.map_manager = map_manager
        self.map_name = None
        self.coords = pygame.Vector2(0, 0)
        self.move_ease = move_ease
        self.factor = 1


    def set_map(self, map_name) -> None:
        """
        permet de définir quel map afficher
        """
        self.map_name = map_name

    def move(self, dt: float, coords: pygame.Vector2, teleport: bool=False) -> None:
        """
            Mettre a jour les coordonnés sur la map
        """
        if teleport:
            self.coords.x = coords.x
            self.coords.y = coords.y
        else: # On applique le "ease" (on adoucie le déplacement)
            self.coords.x += (coords.x - self.coords.x) * (min((dt * self.move_ease * self.factor), 1))
            self.coords.y += (coords.y - self.coords.y) * (min((dt * self.move_ease * self.factor), 1))

    def set_zoom(self, factor: float) -> None:
        # si le facteur de zoom a changé, on recalcul en fonction un zoom utilisable
        if self.factor != factor:
            # on récupère un bon facteur
            self.factor = round(factor*16)/16

    def draw(self, draw_surface: pygame.Surface, player) -> None:
        """
        permet d'afficher / de dessiner la map
        """

        map = self.map_manager.get_map(self.map_name)

        # constantes utiles
        tile_size = self.map_manager.get_map(self.map_name).tilewidth

        tile_size_factor = tile_size * self.factor

        half_width = draw_surface.get_width() / 2
        half_height = draw_surface.get_height() / 2

        x_const = half_width / (tile_size_factor)
        y_const = half_height / (tile_size_factor)

        # déplacement des tiles suivant la position de la caméra
        offset_x = math.floor(-self.coords.x * tile_size_factor + half_width)
        offset_y = math.floor(-self.coords.y * tile_size_factor + half_height)
        
        # calcul de la zone à afficher
        minx = math.floor(self.coords.x - x_const)
        maxx = math.ceil(self.coords.x + x_const) + 1

        miny = math.floor(self.coords.y - y_const)
        maxy = math.ceil(self.coords.y + y_const) + 1

        # on récupère les coordonnées du joueur
        player_pos = pygame.Vector2(math.floor(player.pos.x * tile_size_factor) + offset_x, math.floor(player.pos.y * tile_size_factor) + offset_y)

        # on récupère toutes les tiles qui seront à afficher à cette frame
        tiles = []

        for layer_index, layer in enumerate(map.layers):
            for y in range(max(miny, 0), min(maxy, map.height)):
                for x in range(max(minx, 0), min(maxx, map.width)):
                    if layer.visible :# or layer.properties["collide"] == True
                        # récupération de l'image de la tile
                        tile_image = map.get_tile_image(x, y, layer_index)
                        if tile_image is not None:
                            # calcul de la position sur l'écran de la tile
                            posx = x * tile_size_factor + offset_x
                            posy = y * tile_size_factor + offset_y

                            # ajout de la tile à la liste des tiles à afficher
                            tiles.append((tile_image.get_image(self.factor), (posx, posy)))
                    # permet de mettre le joueur sur le bon layer

                if layer.name == "walls" and math.floor(player.pos.y) == y:
                    
                    tiles.append((player.get_animation(self.factor),(player_pos)))
        
        # On met la couleur de fond de la map
        draw_surface.fill(map.background_color)

        # On dessine toutes les tiles
        draw_surface.blits(tiles, doreturn=False)
        
        # du debug en plus

        #player_rect = player.get_rect()
        #print((player_pos.x, player_pos.y, player_rect.width * tile_size_factor, player_rect.height * tile_size_factor))
        #pygame.draw.rect(draw_surface,"red",pygame.Rect(player_pos.x, player_pos.y,1*tile_size_factor,1*tile_size_factor))
        
        
    


        
        