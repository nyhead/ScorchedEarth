import math
from game_state import *
class Projectile:
	def __init__(self, pos,vel,col,explosion_radius,canvas):
		self.pos = pos
		self.vel = vel
		self.color = col
		self.explosion_radius = explosion_radius
		self.is_dead = False
		self.projectile = None
		self.ball_size= TANK_SIZE/2
		self.canvas = canvas

		self.draw()

	def draw(self):
		if self.projectile is None:
			self.canvas.delete(self.projectile)

		self.projectile = self.canvas.create_oval(self.pos.x-self.ball_size,self.pos.y-self.ball_size,self.pos.x+self.ball_size,self.pos.y+self.ball_size,fill=self.color,width = 3)

