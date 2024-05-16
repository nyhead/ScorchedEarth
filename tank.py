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
	def __init__(self, pos: Pos, color, canvas):
		self.canvas = canvas
		self.pos = pos
		self.color = color
		self.size = TANK_SIZE
		self.id = None

	def rotate(self, angle_degrees, length, x, y):
		angle_radians = angle_degrees * math.pi / 180
		endx = x + length * math.cos(angle_radians)
		endy = y + length * math.sin(angle_radians)
		return endx, endy

	def draw(self):
		if self.id:
			self.canvas.delete(self.id)
		x1 = self.pos.x - self.size
		y1 = self.pos.y - self.size / 2
		x2 = self.pos.x + self.size
		y2 = self.pos.y + self.size / 2
		#rotating a line, aiming
		#in Tkinter's coordinate system:
		#Increasing the y-coordinate actually moves down the screen,
		# which effectively reverses the direction of the positive y-axis compared to the
		# standard Cartesian coordinate system.
		x,y = self.pos.x, self.pos.y
		angle = 60
		endx, endy = self.rotate(360-angle, 12, x, y)  # Assuming length is 100
		self.canvas.create_line(x, y, endx, endy, fill=self.color, width=3)

		self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
