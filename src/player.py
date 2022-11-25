import pygame
import math

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 10

    def get_rect(self):
        print(pygame.Rect(self.pos.x, self.pos.y, 1, 1))
        return pygame.Rect(self.pos.x, self.pos.y, 1, 1)

    def get_hitbox(self):
        return pygame.Rect(self.pos.x, self.pos.y + 0.25, 1, 0.5)

    def move(self, map_manager, dt: float):
        if self.direction.magnitude() != 0:
            collisions_tiles = map_manager.get_around_collisions("map",self.pos, 1, ["collisions"])["collisions"]
            print(self.pos, collisions_tiles)
            velocity = self.direction.normalize() * self.speed * dt
            #self.pos += velocity
            
            step = max(math.ceil(abs(velocity.y)), math.ceil(abs(velocity.x)))
            for i in range(step):
                self.pos.x += velocity.x / step
                self.collisions("x", velocity, collisions_tiles)
            for i in range(step):
                self.pos.y += velocity.y / step
                self.collisions("y", velocity, collisions_tiles)
                
    def collisions(self, direction: str, velocity: float, collisions: list) -> pygame.Vector2:
        for tile_pos in collisions:
            tile_rect = pygame.Rect(tile_pos[0], tile_pos[1], 1, 1)
            
            if tile_rect.colliderect(self.get_rect()):
                #print("collisions", tile_rect)
                if direction == "y":
                    if velocity.y > 0: # moving down
                        self.pos.y = tile_rect.y - 1
                    elif velocity.y < 0: # moving up
                        self.pos.y = tile_rect.y + 1
                        
                elif direction == "x":   
                    if velocity.x > 0: # moving right
                        self.pos.x = tile_rect.x - 1

                    elif velocity.x < 0: # moving left
                        self.pos.x = tile_rect.x + 1
            

    def event_handler(self, event: pygame.event):
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
            