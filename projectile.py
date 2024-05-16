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
		self.canvas = canvas

	def draw(self):
		if self.projectile is None:
			self.canvas.delete(self.projectile)

		self.projectile = self.canvas.create_oval(self.pos.x-TANK_SIZE,self.pos.y-TANK_SIZE,self.pos.x+TANK_SIZE,self.pos.y+TANK_SIZE,fill=self.color,width = 3)

	def animate_projectile(self):
		gravity = 1  # Acceleration due to gravity
		time_interval = 0.05  # Time step for the simulation

		# Update horizontal position
		self.pos.x += self.vel.x * time_interval

		# Update vertical position
		self.pos.y += self.vel.y * time_interval + 0.5 * gravity * time_interval ** 2

		# Update vertical velocity
		self.vel.y += gravity * time_interval

		# Update projectile position on canvas
		self.canvas.coords(self.projectile, self.pos.x - TANK_SIZE, self.pos.y - TANK_SIZE, self.pos.x + TANK_SIZE,
						   self.pos.y + TANK_SIZE)

		# Schedule the next update
		self.canvas.after(int(time_interval * 100), self.animate_projectile)