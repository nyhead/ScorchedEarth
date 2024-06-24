from game_state import *
from collections import OrderedDict
import heapq


class HallOfFame:
	def __init__(self):
		self.hall = []
		heapq.heapify(self.hall)
		self.name_to_score = {}
		self.limit = 10

	def update(self, name, score):
		print(name, score)
		if name in self.name_to_score:
			# Update the score if it's higher
			if score > self.name_to_score[name]:
				self.hall.remove((self.name_to_score[name], name))
				self.name_to_score[name] = score

				heapq.heappush(self.hall, (score, name))
		else:
			# Add the new name and score
			self.name_to_score[name] = score
			heapq.heappush(self.hall, (score, name))

		# Maintain the size of the heap
		if len(self.hall) > self.limit:
			removed_score, removed_name = heapq.heappop(self.hall)
			del self.name_to_score[removed_name]

		# Ensure the heap property is maintained
		heapq.heapify(self.hall)

