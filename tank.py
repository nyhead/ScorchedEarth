import tkinter as tk
from typing import Tuple
from game_state import *
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

	def draw(self):
		if self.id:
			self.canvas.delete(self.id)
		x1 = self.pos.x - self.size
		y1 = self.pos.y - self.size / 2
		x2 = self.pos.x + self.size
		y2 = self.pos.y + self.size / 2
		self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
