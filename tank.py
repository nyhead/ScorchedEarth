import math
import tkinter as tk
from typing import Tuple
from game_state import *
from PIL import Image, ImageDraw
class Pos:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Tank:
	def __init__(self, pos: Pos, color, canvas,angle=45):
		self.canvas = canvas
		self.pos = pos
		self.color = color
		self.size = TANK_SIZE
		self.angle = angle
		self.turret_length = 12
		self.turret_base = pos
		self.id = None
		self.turret = None

	def rotate(self):
		angle_radians = self.angle * math.pi / 180
		endx = self.turret_base.x + self.turret_length * math.cos(angle_radians)
		endy = self.turret_base.y - self.turret_length * math.sin(angle_radians)
		return endx, endy

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
		endx, endy = self.rotate()
		self.turret = self.canvas.create_line(self.turret_base.x, self.turret_base.y, endx, endy, fill=self.color, width=3)

		self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)


	def set_angle(self, angle):
		self.angle -= angle
		self.update_turret()


	def update_turret(self):
		endx,endy=self.rotate()
		self.canvas.coords(self.turret, self.turret_base.x, self.turret_base.y, endx, endy)