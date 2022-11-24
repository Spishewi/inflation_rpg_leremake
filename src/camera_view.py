import pygame
from map_manager import MapManager
import math

class CameraView:
    """
    permet d'afficher une partie d'une map
    """
    def __init__(self, map_manager: MapManager, move_ease: float) -> None:

        
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
        else:
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
        #draw_surface.fill((0, 0, 0))

        map = self.map_manager.get_map(self.map_name)

        tile_size = self.map_manager.get_map(self.map_name).tilewidth

        tile_size_factor = tile_size * self.factor

        half_width = draw_surface.get_width() / 2
        half_height = draw_surface.get_height() / 2

        x_const = half_width / (tile_size_factor)
        y_const = half_height / (tile_size_factor)

        x_const_2 = -self.coords.x * tile_size_factor + half_width
        y_const_2 = -self.coords.y * tile_size_factor + half_height
        
        minx = math.floor(self.coords.x - x_const)
        maxx = math.ceil(self.coords.x + x_const) + 1

        miny = math.floor(self.coords.y - y_const)
        maxy = math.ceil(self.coords.y + y_const) + 1

        tiles = []
        for x in range(max(minx, 0), min(maxx, map.width)):
            for y in range(max(miny, 0), min(maxy, map.height)):
                for layer_index in range(len(map.layers)-1, -1, -1):
                    tile_image = map.get_tile_image(x, y, layer_index)
                    if tile_image is not None:
                        posx = x * tile_size_factor + x_const_2
                        posy = y * tile_size_factor + y_const_2
                        #draw_surface.blit(tile_image.get_image(self.factor), (posx, posy))
                        tiles.append((tile_image.get_image(self.factor), (posx, posy)))
                        if tile_image.opaque:
                            break
        tiles.reverse()
        #for entity in entities:
            #tiles.append((entity.image, (entity.rect.x*self.factor* tile_size_factor + x_const_2, entity.rect.y*self.factor* tile_size_factor + y_const_2)))
        draw_surface.blits(tiles, doreturn=False)
        player_rect = player.get_rect()
        player_pos = pygame.Vector2(player_rect.x * self.factor + x_const_2, player_rect.y * self.factor + y_const_2)
        print((player_pos.x, player_pos.y, player_rect.width * self.factor, player_rect.height * self.factor))
        pygame.draw.rect(draw_surface, "red", (player_pos.x, player_pos.y, player_rect.width * self.factor, player_rect.height * self.factor))
        


        
        