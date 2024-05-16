import math
from game_state import *
import projectile


class Tank:
	def __init__(self, pos: Pos, color, canvas,angle=90):
		self.canvas = canvas
		self.pos = pos
		self.color = color
		self.size = TANK_SIZE
		self.angle = angle
		self.turret_length = 6
		self.id = None
		self.turret = None
		self.turret_base = Pos(self.pos.x, self.pos.y - TANK_SIZE/2)
		self.turret_end = Pos(*rotate(self.turret_base.x,self.turret_base.y, self.angle,self.turret_length))
		self.power = 20
	def draw(self):
		if self.id:
			self.canvas.delete(self.id)
		if self.turret:
			self.canvas.delete(self.turret)
		x1 = self.pos.x - self.size
		y1 = self.pos.y - self.size / 2
		x2 = self.pos.x + self.size
		y2 = self.pos.y + self.size / 2
		#rotating a line, aiming
		self.turret_end = Pos(*rotate(self.turret_base.x,self.turret_base.y, self.angle,self.turret_length))
		self.turret = self.canvas.create_line(self.turret_base.x, self.turret_base.y, self.turret_end.x, self.turret_end.y, fill=self.color, width=3)

		self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)


	def rotate_turret(self, angle):
		if (0 <= self.angle - angle <= 180):
			self.angle -= angle
			self.update_turret()


	def update_turret(self):
		self.turret_end = Pos(*rotate(self.turret_base.x,self.turret_base.y, self.angle,self.turret_length))
		self.canvas.coords(self.turret, self.turret_base.x, self.turret_base.y, self.turret_end.x, self.turret_end.y)
	def fire_projectile(self):
		velx = self.power * math.cos(math.radians(self.angle))
		vely = -self.power * math.sin(math.radians(self.angle))
		p = projectile.Projectile(Pos(self.turret_end.x, self.turret_end.y-TANK_SIZE) , Pos(velx, vely), self.color, 20, self.canvas)
		# p.draw()
		# p.animate_projectile()
