import pygame
import math

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 20

    def get_rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, 16, 16)

    def get_hitbox(self):
        return pygame.Rect(self.pos.x, self.pos.y + 4, 16, 8)

    def move(self, map_manager, dt: float):
        if self.direction.magnitude() != 0:
            collisions_tiles = map_manager.get_around_collisions("map",self.pos, 3, ["collisions"])["collisions"]
            velocity = self.direction.normalize() * self.speed * dt
            step = max(math.ceil(abs(velocity.y / 16)), math.ceil(abs(velocity.x / 16)))
            new_pos = self.pos.copy()
            for i in range(step):
                new_pos += velocity / step
                self.collisions(velocity, collisions_tiles)

    def collisions(self, velocity: float, collisions: list) -> pygame.Vector2:
        for tile_pos in collisions:
            print(tile_pos[0], tile_pos[1], 16, 16)
            tile_rect = pygame.Rect(tile_pos[0], tile_pos[1], 16, 16)
            if tile_rect.colliderect(self.get_rect()):
                if velocity.y > 0: # moving down
                    self.pos.y = tile_rect.y - 16
                elif velocity.y < 0: # moving up
                    self.pos.y = tile_rect.y + 16
                    
                if velocity.x > 0: # moving right
                    self.pos.x = tile_rect.x - 16

                elif velocity.x < 0: # moving left
                    self.pos.x = tile_rect.x+ 16
    def event_handler(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction.x -= 1
            elif event.key == pygame.K_RIGHT:
                self.direction.x += 1
            elif event.key == pygame.K_UP:
                self.direction.y -= 1
            elif event.key == pygame.K_DOWN:
                self.direction.y += 1
            