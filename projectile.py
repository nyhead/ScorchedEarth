import math
from game_state import *
class Projectile:
	def __init__(self, pos,vel,col,explosion_radius,canvas):
		self.pos = pos
		self.vel = vel
		self.col = col
		self.explosion_radius = explosion_radius
		self.is_dead = False
		self.projectile = None
		self.canvas = canvas

	def draw(self, canvas):
		if self.projectile is None:
			self.canvas.delete(self.projectile)


