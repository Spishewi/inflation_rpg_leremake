from __future__ import annotations # psq sinon il aimait pas certains type hint
import pygame

class Hitbox:
	def __init__(self, x: float, y: float, width: float, height: float):
		"""
		classe pour permettre de faire des collisions comme avec les rect de pygame, mais avec des virgules.
		"""

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
		"""
		retourne True si les hitbox se touche où overlap.
		"""
		if not (self.x <= hitbox.x <= self.x + self.width or hitbox.x <= self.x <= hitbox.x + hitbox.width):
			return False
		if not (self.y <= hitbox.y <= self.y + self.height or hitbox.y <= self.y <= hitbox.y + hitbox.height):
			return False
		return True

	def overlap(self, hitbox: Hitbox) -> bool:
		"""
		retourne True si les hitbox overlap, mais False s'y elles se touchent juste.
		"""
		if not (self.x < hitbox.x < self.x + self.width or hitbox.x < self.x < hitbox.x + hitbox.width):
			return False
		if not (self.y < hitbox.y < self.y + self.height or hitbox.y < self.y < hitbox.y + hitbox.height):
			return False
		return True

	def __str__(self):
		return f"{self.__class__.__name__} ({self.x}, {self.y}, {self.width}, {self.height})"

	def __repr__(self):
		return str(self)

	@staticmethod
	def from_pygame_rect(rect: pygame.Rect) -> Hitbox:
		return Hitbox(rect.x, rect.y, rect.width, rect.height)