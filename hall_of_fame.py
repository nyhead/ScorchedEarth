from util import *
from collections import OrderedDict
import heapq

class HallOfFame:
	def __init__(self):
		self.hall = {}
		self.limit = 10

	def update(self, name, score):
		print(name, score)
		# Maintain the size
		if len(self.hall.items()) >= self.limit:
			self.hall.popitem()
		if name in self.hall:
			# Update the score if it's higher
			if score > self.hall[name]:
				self.hall[name] = score
		else:
			# Add the new name and score
			self.hall[name] = score

	def get_hall(self):
		return sorted(self.hall.items(), key=lambda x:x[1], reverse=True)


